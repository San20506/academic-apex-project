#!/usr/bin/env python3
"""
Academic Apex Strategist - FastAPI Backend

Main FastAPI application providing REST API endpoints for the 
Academic Apex educational platform.
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ValidationError

# Import our components
from ollama_adapter import OllamaAdapter
from obsidian_adapter import ObsidianAdapter
from ingestion_pipeline import IngestionPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Academic Apex Strategist API",
    description="AI-powered educational content generation platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
config = {
    'ollama_host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
    'curator_url': os.getenv('CURATOR_SERVICE_URL', 'http://localhost:5001'),
    'vault_path': os.getenv('OBSIDIAN_VAULT_PATH', ''),
    'default_model': os.getenv('DEFAULT_MODEL', 'mistral:7b'),
    'upload_dir': Path(os.getenv('UPLOAD_DIR', 'uploads')),
    'generated_dir': Path(os.getenv('GENERATED_DIR', 'generated'))
}

# Create directories
config['upload_dir'].mkdir(exist_ok=True)
config['generated_dir'].mkdir(exist_ok=True)

# Initialize adapters
ollama_adapter = OllamaAdapter(base_url=config['ollama_host'], model=config['default_model'])
obsidian_adapter = None
ingestion_pipeline = IngestionPipeline()

if config['vault_path']:
    try:
        obsidian_adapter = ObsidianAdapter(config['vault_path'])
        logger.info(f"✓ Obsidian adapter initialized: {config['vault_path']}")
    except Exception as e:
        logger.error(f"✗ Failed to initialize Obsidian adapter: {e}")

# Pydantic models
class SystemStatus(BaseModel):
    ollama_connected: bool
    curator_running: bool
    obsidian_configured: bool
    models_available: List[str]
    issues: List[str]
    last_check: str

class QuizRequest(BaseModel):
    subject: str
    difficulty: str = "intermediate"
    num_questions: int = 10
    use_curation: bool = True

class StudyPlanRequest(BaseModel):
    subject: str
    duration: str = "2 hours"
    difficulty: str = "intermediate"
    objectives: List[str] = []
    use_curation: bool = True

class CodeRequest(BaseModel):
    module_name: str = "study_utils"
    functionality: str
    include_tests: bool = True
    use_curation: bool = True

class GeneratedContent(BaseModel):
    id: str
    type: str
    subject: str
    content: str
    filename: str
    created_at: str
    metadata: Dict[str, Any]

# Global status cache
system_status_cache = {
    'data': None,
    'last_update': None
}

async def check_system_health() -> SystemStatus:
    """Check the health of all system components."""
    status_data = {
        'ollama_connected': False,
        'curator_running': False,
        'obsidian_configured': bool(obsidian_adapter),
        'models_available': [],
        'issues': [],
        'last_check': datetime.now().isoformat()
    }
    
    try:
        # Check Ollama
        status_data['ollama_connected'] = ollama_adapter.test_connection()
        if status_data['ollama_connected']:
            models_info = ollama_adapter.list_models()
            status_data['models_available'] = [m.get('name', '') for m in models_info.get('models', [])]
        else:
            status_data['issues'].append('Ollama service not reachable')
            
    except Exception as e:
        status_data['issues'].append(f'Ollama check failed: {str(e)}')
    
    try:
        # Check Curator Service
        import requests
        response = requests.get(f"{config['curator_url']}/healthz", timeout=5)
        status_data['curator_running'] = response.status_code == 200
        if not status_data['curator_running']:
            status_data['issues'].append('Curator service not responding')
    except Exception as e:
        status_data['issues'].append(f'Curator service unreachable: {str(e)}')
    
    # Check Obsidian
    if obsidian_adapter:
        try:
            validation = obsidian_adapter.validate_vault()
            if not validation.get('valid'):
                status_data['issues'].extend(validation.get('issues', []))
        except Exception as e:
            status_data['issues'].append(f'Obsidian vault issue: {str(e)}')
    else:
        status_data['issues'].append('Obsidian vault not configured (set OBSIDIAN_VAULT_PATH)')
    
    return SystemStatus(**status_data)

async def curate_prompt(prompt: str, instruction: str = "") -> str:
    """Curate a prompt using the curator service."""
    try:
        import requests
        response = requests.post(
            f"{config['curator_url']}/api/curate",
            json={"prompt": prompt, "instruction": instruction},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result.get('refined', prompt)
        
        logger.warning("Prompt curation failed, using original")
        return prompt
        
    except Exception as e:
        logger.warning(f"Prompt curation error: {e}, using original")
        return prompt

# API Routes

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {"message": "Academic Apex Strategist API", "version": "1.0.0"}

@app.get("/api/system-status", response_model=SystemStatus)
async def get_system_status():
    """Get comprehensive system status."""
    # Use cache if recent (within 30 seconds)
    now = datetime.now()
    if (system_status_cache['data'] and 
        system_status_cache['last_update'] and
        (now - system_status_cache['last_update']).total_seconds() < 30):
        return system_status_cache['data']
    
    # Update cache
    status = await check_system_health()
    system_status_cache['data'] = status
    system_status_cache['last_update'] = now
    
    return status

@app.post("/api/generate-quiz")
async def generate_quiz(request: QuizRequest, background_tasks: BackgroundTasks):
    """Generate a diagnostic quiz."""
    try:
        # Build quiz prompt
        quiz_prompt = f"""Create a {request.difficulty} level diagnostic quiz for {request.subject} with exactly {request.num_questions} questions.

Requirements:
- Include a mix of multiple choice, short answer, and essay questions
- Cover fundamental concepts and practical applications
- Provide clear instructions for each section
- End with "---ANSWERS---" section containing detailed answer explanations
- Format professionally for educational use
- Make questions challenging but fair for {request.difficulty} level learners

Subject focus: {request.subject}
Target difficulty: {request.difficulty}
Number of questions: {request.num_questions}

Create a comprehensive assessment that thoroughly evaluates understanding."""

        # Curate prompt if enabled
        if request.use_curation:
            quiz_prompt = await curate_prompt(
                quiz_prompt,
                "Optimize this prompt for generating high-quality educational quizzes"
            )
        
        # Generate quiz
        logger.info(f"Generating quiz for {request.subject} ({request.difficulty}, {request.num_questions} questions)")
        result = ollama_adapter.generate(
            quiz_prompt,
            max_tokens=2000,
            temperature=0.6
        )
        
        quiz_content = result["text"].strip()
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_{request.subject.replace(' ', '_').lower()}_{timestamp}.md"
        
        # Save to generated folder
        file_path = config['generated_dir'] / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Quiz: {request.subject}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Difficulty:** {request.difficulty}\n")
            f.write(f"**Questions:** {request.num_questions}\n")
            f.write(f"**Model:** {result.get('model', 'unknown')}\n\n")
            f.write("---\n\n")
            f.write(quiz_content)
        
        # Save to Obsidian if configured
        obsidian_saved = False
        if obsidian_adapter:
            try:
                obs_result = obsidian_adapter.create_quiz_note(request.subject, quiz_content)
                obsidian_saved = obs_result.get('success', False)
            except Exception as e:
                logger.warning(f"Failed to save to Obsidian: {e}")
        
        return {
            'success': True,
            'content': quiz_content,
            'filename': filename,
            'obsidian_saved': obsidian_saved,
            'stats': {
                'length': len(quiz_content),
                'model': result.get('model'),
                'tokens': result.get('completion_tokens', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Quiz generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-study-plan")
async def generate_study_plan(request: StudyPlanRequest):
    """Generate a study plan."""
    try:
        # Format objectives
        objectives_text = "\n".join([f"- {obj}" for obj in request.objectives if obj.strip()])
        if not objectives_text:
            objectives_text = f"- Master core concepts of {request.subject}\n- Apply knowledge practically\n- Build strong foundation"
        
        # Build study plan prompt
        study_prompt = f"""Create a comprehensive {request.duration} study plan for "{request.subject}" at {request.difficulty} level.

Requirements:
- Break down into specific time blocks with exact timing (e.g., "0:00-0:15 - Introduction")
- Include variety: reading, hands-on practice, review, strategic breaks
- Add progress checkpoints and self-assessment moments
- Use active learning techniques and spaced repetition
- Format as clear markdown with timeline structure
- Include specific activities and resources for each time block
- Add motivational elements and difficulty progression

Subject: {request.subject}
Duration: {request.duration}
Level: {request.difficulty}

Learning Objectives:
{objectives_text}

Create a detailed minute-by-minute timeline that maximizes learning effectiveness and retention."""

        # Curate prompt if enabled
        if request.use_curation:
            study_prompt = await curate_prompt(
                study_prompt,
                "Optimize this prompt for creating effective, engaging study plans"
            )
        
        # Generate study plan
        logger.info(f"Generating study plan for {request.subject} ({request.duration}, {request.difficulty})")
        result = ollama_adapter.generate(
            study_prompt,
            max_tokens=2500,
            temperature=0.5
        )
        
        plan_content = result["text"].strip()
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"study_plan_{request.subject.replace(' ', '_').lower()}_{timestamp}.md"
        
        # Save to generated folder
        file_path = config['generated_dir'] / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Study Plan: {request.subject}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Duration:** {request.duration}\n")
            f.write(f"**Level:** {request.difficulty}\n")
            f.write(f"**Model:** {result.get('model', 'unknown')}\n\n")
            f.write("## Learning Objectives\n\n")
            f.write(objectives_text + "\n\n")
            f.write("---\n\n")
            f.write(plan_content)
        
        # Save to Obsidian if configured
        obsidian_saved = False
        if obsidian_adapter:
            try:
                obs_result = obsidian_adapter.create_study_plan_note(
                    request.subject, plan_content, request.duration
                )
                obsidian_saved = obs_result.get('success', False)
            except Exception as e:
                logger.warning(f"Failed to save to Obsidian: {e}")
        
        return {
            'success': True,
            'content': plan_content,
            'filename': filename,
            'obsidian_saved': obsidian_saved,
            'stats': {
                'length': len(plan_content),
                'model': result.get('model'),
                'tokens': result.get('completion_tokens', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Study plan generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-code")
async def generate_code(request: CodeRequest):
    """Generate Python code module."""
    try:
        # Build code generation prompt
        code_prompt = f"""Create a complete Python module named '{request.module_name}' that provides {request.functionality}.

Requirements:
- Write complete, runnable Python code
- Include comprehensive docstrings for all functions and classes
- Add type hints where appropriate
- Include proper error handling and input validation
- Follow PEP 8 style guidelines
- Make functions practical for real academic/educational use
- Add logging where appropriate
- Include usage examples in docstrings

Include unit tests: {request.include_tests}

Focus on creating clean, maintainable code that would be useful for students and educators. The module should be production-ready with clear documentation and robust error handling."""

        # Curate prompt if enabled
        if request.use_curation:
            code_prompt = await curate_prompt(
                code_prompt,
                "Optimize this prompt for generating high-quality, educational Python code"
            )
        
        # Generate code
        logger.info(f"Generating Python module: {request.module_name}")
        result = ollama_adapter.generate(
            code_prompt,
            max_tokens=3000,
            temperature=0.3
        )
        
        code_content = result["text"].strip()
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{request.module_name}_{timestamp}.py"
        
        # Save to generated folder
        file_path = config['generated_dir'] / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'"""\n{request.module_name} - Generated by Academic Apex Strategist\n\n')
            f.write(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Functionality: {request.functionality}\n')
            f.write(f'Model: {result.get("model", "unknown")}\n')
            f.write('"""\n\n')
            f.write(code_content)
        
        # Test syntax
        syntax_valid = False
        syntax_error = None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), filename, 'exec')
            syntax_valid = True
        except SyntaxError as e:
            syntax_error = f"Line {e.lineno}: {e.msg}"
        except Exception as e:
            syntax_error = str(e)
        
        return {
            'success': True,
            'content': code_content,
            'filename': filename,
            'syntax_valid': syntax_valid,
            'syntax_error': syntax_error,
            'stats': {
                'length': len(code_content),
                'model': result.get('model'),
                'tokens': result.get('completion_tokens', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document with OCR."""
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'text/plain']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type {file.content_type} not supported")
        
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = config['upload_dir'] / safe_filename
        
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Process with ingestion pipeline
        result = await ingestion_pipeline.process_document(file_path)
        
        return {
            'success': True,
            'filename': safe_filename,
            'extracted_text': result.get('text', ''),
            'confidence': result.get('confidence', 0),
            'processing_time': result.get('processing_time', 0),
            'file_size': len(content)
        }
        
    except Exception as e:
        logger.error(f"Document upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files")
async def list_files():
    """List generated files."""
    try:
        files = []
        
        if config['generated_dir'].exists():
            for file_path in config['generated_dir'].glob("*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        'name': file_path.name,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'type': file_path.suffix[1:] if file_path.suffix else 'unknown'
                    })
        
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return {
            'success': True,
            'files': files,
            'total': len(files)
        }
        
    except Exception as e:
        logger.error(f"File listing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{filename}")
async def get_file_content(filename: str):
    """Get content of a generated file."""
    try:
        file_path = config['generated_dir'] / filename
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'success': True,
            'filename': filename,
            'content': content,
            'size': len(content)
        }
        
    except Exception as e:
        logger.error(f"File content error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("🚀 Academic Apex Strategist API starting up...")
    
    # Test connections
    if ollama_adapter.test_connection():
        logger.info("✓ Ollama connection successful")
    else:
        logger.warning("✗ Ollama connection failed")
    
    logger.info("✅ FastAPI backend ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
