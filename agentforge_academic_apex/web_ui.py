#!/usr/bin/env python3
"""
Web UI for Academic Apex Strategist

MIT License - Academic Apex Project

A modern, user-friendly web interface for creating study plans, quizzes, 
and educational content using local AI models.
"""

import os
import json
import logging
import requests
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.serving import make_server

# Import our components
from ollama_adapter import OllamaAdapter
from obsidian_adapter import ObsidianAdapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'academic_apex_secret_key_2025'  # Change in production

# Global configuration
config = {
    'ollama_host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
    'curator_url': os.getenv('CURATOR_SERVICE_URL', 'http://localhost:5001'),
    'vault_path': os.getenv('OBSIDIAN_VAULT_PATH', ''),
    'app_port': int(os.getenv('WEB_UI_PORT', '5000')),
    'debug_mode': os.getenv('DEBUG', 'false').lower() == 'true'
}

# Initialize adapters
ollama_adapter = OllamaAdapter(base_url=config['ollama_host'])
obsidian_adapter = None

# Setup Obsidian adapter if vault path is configured
if config['vault_path']:
    try:
        obsidian_adapter = ObsidianAdapter(config['vault_path'])
        logger.info(f"✓ Obsidian adapter initialized: {config['vault_path']}")
    except Exception as e:
        logger.error(f"✗ Failed to initialize Obsidian adapter: {e}")

# Create directories
Path("generated").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# System status cache
system_status = {
    'ollama_connected': False,
    'curator_running': False,
    'obsidian_configured': bool(obsidian_adapter),
    'last_check': None
}


def check_system_health() -> Dict[str, Any]:
    """Check the health of all system components."""
    status = {
        'ollama_connected': False,
        'curator_running': False,
        'obsidian_configured': bool(obsidian_adapter),
        'models_available': [],
        'issues': []
    }
    
    try:
        # Check Ollama
        status['ollama_connected'] = ollama_adapter.test_connection()
        if status['ollama_connected']:
            models_info = ollama_adapter.list_models()
            status['models_available'] = [m.get('name', '') for m in models_info.get('models', [])]
        else:
            status['issues'].append('Ollama service not reachable')
            
    except Exception as e:
        status['issues'].append(f'Ollama check failed: {str(e)}')
    
    try:
        # Check Curator Service
        response = requests.get(f"{config['curator_url']}/healthz", timeout=5)
        status['curator_running'] = response.status_code == 200
        if not status['curator_running']:
            status['issues'].append('Curator service not responding')
    except Exception as e:
        status['issues'].append(f'Curator service unreachable: {str(e)}')
    
    # Check Obsidian
    if obsidian_adapter:
        try:
            validation = obsidian_adapter.validate_vault()
            if not validation.get('valid'):
                status['issues'].extend(validation.get('issues', []))
        except Exception as e:
            status['issues'].append(f'Obsidian vault issue: {str(e)}')
    else:
        status['issues'].append('Obsidian vault not configured (set OBSIDIAN_VAULT_PATH)')
    
    status['last_check'] = datetime.now().isoformat()
    return status


def curate_prompt(prompt: str, instruction: str = "") -> str:
    """Curate a prompt using the curator service."""
    try:
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


@app.route('/')
def index():
    """Main dashboard page."""
    status = check_system_health()
    return render_template('dashboard.html', 
                         status=status, 
                         config=config,
                         vault_configured=bool(obsidian_adapter))


@app.route('/api/system-status')
def api_system_status():
    """API endpoint for system status."""
    return jsonify(check_system_health())


@app.route('/generate-quiz', methods=['GET', 'POST'])
def generate_quiz():
    """Quiz generation page and handler."""
    if request.method == 'POST':
        try:
            data = request.get_json()
            subject = data.get('subject', '').strip()
            difficulty = data.get('difficulty', 'intermediate')
            num_questions = int(data.get('num_questions', 10))
            use_curation = data.get('use_curation', True)
            
            if not subject:
                return jsonify({'success': False, 'error': 'Subject is required'}), 400
            
            # Build quiz prompt
            quiz_prompt = f"""Create a {difficulty} level diagnostic quiz for {subject} with exactly {num_questions} questions.

Requirements:
- Include a mix of multiple choice, short answer, and essay questions
- Cover fundamental concepts and practical applications
- Provide clear instructions for each section
- End with "---ANSWERS---" section containing detailed answer explanations
- Format professionally for educational use
- Make questions challenging but fair for {difficulty} level learners

Subject focus: {subject}
Target difficulty: {difficulty}
Number of questions: {num_questions}

Create a comprehensive assessment that thoroughly evaluates understanding."""

            # Curate prompt if enabled
            if use_curation:
                quiz_prompt = curate_prompt(
                    quiz_prompt,
                    "Optimize this prompt for generating high-quality educational quizzes"
                )
            
            # Generate quiz
            logger.info(f"Generating quiz for {subject} ({difficulty}, {num_questions} questions)")
            result = ollama_adapter.generate(
                quiz_prompt,
                max_tokens=2000,
                temperature=0.6
            )
            
            quiz_content = result["text"].strip()
            
            # Save to files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"quiz_{subject.replace(' ', '_').lower()}_{timestamp}.md"
            
            # Save to generated folder
            file_path = Path("generated") / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Quiz: {subject}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Difficulty:** {difficulty}\n")
                f.write(f"**Questions:** {num_questions}\n")
                f.write(f"**Model:** {result.get('model', 'unknown')}\n\n")
                f.write("---\n\n")
                f.write(quiz_content)
            
            # Save to Obsidian if configured
            obsidian_saved = False
            if obsidian_adapter:
                try:
                    obs_result = obsidian_adapter.create_quiz_note(subject, quiz_content)
                    obsidian_saved = obs_result.get('success', False)
                except Exception as e:
                    logger.warning(f"Failed to save to Obsidian: {e}")
            
            return jsonify({
                'success': True,
                'content': quiz_content,
                'filename': filename,
                'obsidian_saved': obsidian_saved,
                'stats': {
                    'length': len(quiz_content),
                    'model': result.get('model'),
                    'tokens': result.get('completion_tokens', 0)
                }
            })
            
        except Exception as e:
            logger.error(f"Quiz generation error: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('quiz_generator.html')


@app.route('/generate-study-plan', methods=['GET', 'POST'])
def generate_study_plan():
    """Study plan generation page and handler."""
    if request.method == 'POST':
        try:
            data = request.get_json()
            subject = data.get('subject', '').strip()
            duration = data.get('duration', '2 hours')
            difficulty = data.get('difficulty', 'intermediate')
            objectives = data.get('objectives', [])
            use_curation = data.get('use_curation', True)
            
            if not subject:
                return jsonify({'success': False, 'error': 'Subject is required'}), 400
            
            # Format objectives
            objectives_text = "\n".join([f"- {obj}" for obj in objectives if obj.strip()])
            if not objectives_text:
                objectives_text = f"- Master core concepts of {subject}\n- Apply knowledge practically\n- Build strong foundation"
            
            # Build study plan prompt
            study_prompt = f"""Create a comprehensive {duration} study plan for "{subject}" at {difficulty} level.

Requirements:
- Break down into specific time blocks with exact timing (e.g., "0:00-0:15 - Introduction")
- Include variety: reading, hands-on practice, review, strategic breaks
- Add progress checkpoints and self-assessment moments
- Use active learning techniques and spaced repetition
- Format as clear markdown with timeline structure
- Include specific activities and resources for each time block
- Add motivational elements and difficulty progression

Subject: {subject}
Duration: {duration}
Level: {difficulty}

Learning Objectives:
{objectives_text}

Create a detailed minute-by-minute timeline that maximizes learning effectiveness and retention."""

            # Curate prompt if enabled
            if use_curation:
                study_prompt = curate_prompt(
                    study_prompt,
                    "Optimize this prompt for creating effective, engaging study plans"
                )
            
            # Generate study plan
            logger.info(f"Generating study plan for {subject} ({duration}, {difficulty})")
            result = ollama_adapter.generate(
                study_prompt,
                max_tokens=2500,
                temperature=0.5
            )
            
            plan_content = result["text"].strip()
            
            # Save to files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"study_plan_{subject.replace(' ', '_').lower()}_{timestamp}.md"
            
            # Save to generated folder
            file_path = Path("generated") / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Study Plan: {subject}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Duration:** {duration}\n")
                f.write(f"**Level:** {difficulty}\n")
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
                        subject, plan_content, duration
                    )
                    obsidian_saved = obs_result.get('success', False)
                except Exception as e:
                    logger.warning(f"Failed to save to Obsidian: {e}")
            
            return jsonify({
                'success': True,
                'content': plan_content,
                'filename': filename,
                'obsidian_saved': obsidian_saved,
                'stats': {
                    'length': len(plan_content),
                    'model': result.get('model'),
                    'tokens': result.get('completion_tokens', 0)
                }
            })
            
        except Exception as e:
            logger.error(f"Study plan generation error: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('study_plan_generator.html')


@app.route('/generate-code', methods=['GET', 'POST'])
def generate_code():
    """Code generation page and handler."""
    if request.method == 'POST':
        try:
            data = request.get_json()
            module_name = data.get('module_name', 'study_utils').strip()
            functionality = data.get('functionality', '').strip()
            include_tests = data.get('include_tests', True)
            use_curation = data.get('use_curation', True)
            
            if not functionality:
                return jsonify({'success': False, 'error': 'Functionality description is required'}), 400
            
            # Build code generation prompt
            code_prompt = f"""Create a complete Python module named '{module_name}' that provides {functionality}.

Requirements:
- Write complete, runnable Python code
- Include comprehensive docstrings for all functions and classes
- Add type hints where appropriate
- Include proper error handling and input validation
- Follow PEP 8 style guidelines
- Make functions practical for real academic/educational use
- Add logging where appropriate
- Include usage examples in docstrings

Include unit tests: {include_tests}

Focus on creating clean, maintainable code that would be useful for students and educators. The module should be production-ready with clear documentation and robust error handling."""

            # Curate prompt if enabled
            if use_curation:
                code_prompt = curate_prompt(
                    code_prompt,
                    "Optimize this prompt for generating high-quality, educational Python code"
                )
            
            # Generate code
            logger.info(f"Generating Python module: {module_name}")
            result = ollama_adapter.generate(
                code_prompt,
                max_tokens=3000,
                temperature=0.3
            )
            
            code_content = result["text"].strip()
            
            # Save to files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{module_name}_{timestamp}.py"
            
            # Save to generated folder
            file_path = Path("generated") / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f'"""\n{module_name} - Generated by Academic Apex Strategist\n\n')
                f.write(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
                f.write(f'Functionality: {functionality}\n')
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
            
            return jsonify({
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
            })
            
        except Exception as e:
            logger.error(f"Code generation error: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('code_generator.html')


@app.route('/files')
def list_files():
    """List generated files."""
    files = []
    generated_dir = Path("generated")
    
    if generated_dir.exists():
        for file_path in generated_dir.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'name': file_path.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'type': file_path.suffix[1:] if file_path.suffix else 'unknown'
                })
    
    files.sort(key=lambda x: x['modified'], reverse=True)
    return render_template('files.html', files=files)


@app.route('/download/<filename>')
def download_file(filename):
    """Download a generated file."""
    file_path = Path("generated") / filename
    if file_path.exists() and file_path.is_file():
        return send_file(file_path, as_attachment=True)
    else:
        flash(f"File not found: {filename}", 'error')
        return redirect(url_for('list_files'))


@app.route('/view/<filename>')
def view_file(filename):
    """View a generated file."""
    file_path = Path("generated") / filename
    if file_path.exists() and file_path.is_file():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return render_template('file_viewer.html', 
                                 filename=filename, 
                                 content=content,
                                 file_type=file_path.suffix[1:] if file_path.suffix else 'text')
        except Exception as e:
            flash(f"Error reading file: {e}", 'error')
            return redirect(url_for('list_files'))
    else:
        flash(f"File not found: {filename}", 'error')
        return redirect(url_for('list_files'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings and configuration page."""
    if request.method == 'POST':
        try:
            data = request.get_json()
            # Handle settings updates here
            flash("Settings updated successfully!", 'success')
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('settings.html', config=config)


if __name__ == '__main__':
    print("🚀 Starting Academic Apex Strategist Web UI...")
    print(f"📊 Dashboard: http://localhost:{config['app_port']}")
    print(f"🔧 Ollama: {config['ollama_host']}")
    print(f"🎯 Curator: {config['curator_url']}")
    print(f"📝 Vault: {config['vault_path'] or 'Not configured'}")
    print("="*60)
    
    # Start the Flask app
    app.run(
        host='0.0.0.0',
        port=config['app_port'],
        debug=config['debug_mode'],
        threaded=True
    )
