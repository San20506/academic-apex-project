#!/usr/bin/env python3
"""
Academic Apex Strategist - Streamlit Version
AI-powered educational content generation platform
"""

import streamlit as st
import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
import time

# Set page config
st.set_page_config(
    page_title="Academic Apex Strategist",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our components
try:
    from ollama_adapter import OllamaAdapter
    from obsidian_adapter import ObsidianAdapter
except ImportError:
    st.error("⚠️ Missing required modules. Please ensure all files are uploaded correctly.")
    st.stop()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.generated_content = []
    st.session_state.system_status = None

# Configuration
@st.cache_resource
def get_config():
    return {
        'ollama_host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
        'curator_url': os.getenv('CURATOR_SERVICE_URL', 'http://localhost:5001'),
        'vault_path': os.getenv('OBSIDIAN_VAULT_PATH', ''),
        'default_model': os.getenv('DEFAULT_MODEL', 'mistral:7b'),
    }

# Initialize adapters
@st.cache_resource
def initialize_adapters():
    config = get_config()
    ollama_adapter = OllamaAdapter(base_url=config['ollama_host'], model=config['default_model'])
    
    obsidian_adapter = None
    if config['vault_path']:
        try:
            obsidian_adapter = ObsidianAdapter(config['vault_path'])
            logger.info(f"✓ Obsidian adapter initialized: {config['vault_path']}")
        except Exception as e:
            logger.error(f"✗ Failed to initialize Obsidian adapter: {e}")
    
    return ollama_adapter, obsidian_adapter

ollama_adapter, obsidian_adapter = initialize_adapters()

def check_system_health():
    """Check the health of all system components."""
    config = get_config()
    status = {
        'ollama_connected': False,
        'curator_running': False,
        'obsidian_configured': bool(obsidian_adapter),
        'models_available': [],
        'issues': [],
        'last_check': datetime.now().isoformat()
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
    
    return status

def curate_prompt(prompt: str, instruction: str = "") -> str:
    """Curate a prompt using the curator service."""
    config = get_config()
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
        
        return prompt
    except Exception as e:
        logger.warning(f"Prompt curation error: {e}, using original")
        return prompt

def save_content(content: str, filename: str, content_type: str):
    """Save generated content to file and session state."""
    # Create generated directory if it doesn't exist
    Path("generated").mkdir(exist_ok=True)
    
    filepath = Path("generated") / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Add to session state
    st.session_state.generated_content.append({
        'filename': filename,
        'type': content_type,
        'content': content,
        'created_at': datetime.now().isoformat(),
        'filepath': str(filepath)
    })
    
    # Save to Obsidian if configured
    if obsidian_adapter:
        try:
            obsidian_adapter.save_content(content, filename, content_type)
        except Exception as e:
            logger.error(f"Failed to save to Obsidian: {e}")

# Main App Layout
def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🎓 Academic Apex Strategist")
        st.markdown("*AI-powered educational content generation with local privacy*")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 System Status")
        
        if st.button("🔄 Check System Health", type="primary"):
            with st.spinner("Checking system status..."):
                st.session_state.system_status = check_system_health()
        
        if st.session_state.system_status:
            status = st.session_state.system_status
            
            # Status indicators
            st.metric("🤖 Ollama", "✅ Connected" if status['ollama_connected'] else "❌ Offline")
            st.metric("🎯 Curator", "✅ Running" if status['curator_running'] else "❌ Offline")
            st.metric("📝 Obsidian", "✅ Configured" if status['obsidian_configured'] else "❌ Not Set")
            
            if status['models_available']:
                st.write("**Available Models:**")
                for model in status['models_available']:
                    st.write(f"• {model}")
            
            if status['issues']:
                st.warning("**Issues:**")
                for issue in status['issues']:
                    st.write(f"• {issue}")
        
        st.divider()
        
        # Navigation
        page = st.radio(
            "📂 Navigation",
            ["🏠 Dashboard", "📝 Generate Quiz", "📅 Study Plan", "💻 Code Generator", "📁 File Manager", "⚙️ Settings"],
            index=0
        )
    
    # Main content area
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📝 Generate Quiz":
        show_quiz_generator()
    elif page == "📅 Study Plan":
        show_study_plan_generator()
    elif page == "💻 Code Generator":
        show_code_generator()
    elif page == "📁 File Manager":
        show_file_manager()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    st.header("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Generated Content", len(st.session_state.generated_content))
    
    with col2:
        if st.session_state.system_status:
            models_count = len(st.session_state.system_status.get('models_available', []))
            st.metric("🤖 Available Models", models_count)
    
    with col3:
        if st.session_state.system_status:
            issues_count = len(st.session_state.system_status.get('issues', []))
            st.metric("⚠️ System Issues", issues_count)
    
    st.divider()
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Generate Quiz", type="primary", use_container_width=True):
            st.session_state.page = "📝 Generate Quiz"
            st.rerun()
    
    with col2:
        if st.button("📅 Create Study Plan", type="primary", use_container_width=True):
            st.session_state.page = "📅 Study Plan"
            st.rerun()
    
    with col3:
        if st.button("💻 Generate Code", type="primary", use_container_width=True):
            st.session_state.page = "💻 Code Generator"
            st.rerun()

def show_quiz_generator():
    st.header("📝 Quiz Generator")
    
    with st.form("quiz_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("📚 Subject", placeholder="e.g., Python Programming Basics")
            difficulty = st.selectbox("🎯 Difficulty", ["beginner", "intermediate", "advanced"])
        
        with col2:
            num_questions = st.number_input("🔢 Number of Questions", min_value=1, max_value=50, value=10)
            use_curation = st.checkbox("✨ Use Prompt Curation", value=True)
        
        submitted = st.form_submit_button("🎯 Generate Quiz", type="primary")
        
        if submitted and subject:
            with st.spinner(f"Generating {difficulty} quiz for {subject}..."):
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
                
                try:
                    # Generate quiz
                    result = ollama_adapter.generate(
                        quiz_prompt,
                        max_tokens=2000,
                        temperature=0.7
                    )
                    
                    if result.get('success'):
                        content = result['content']
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"quiz_{subject.lower().replace(' ', '_')}_{timestamp}.md"
                        
                        # Save content
                        save_content(content, filename, "quiz")
                        
                        st.success("✅ Quiz generated successfully!")
                        
                        # Display the quiz
                        st.subheader("📝 Generated Quiz")
                        st.markdown(content)
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Quiz",
                            data=content,
                            file_name=filename,
                            mime="text/markdown"
                        )
                        
                    else:
                        st.error(f"❌ Failed to generate quiz: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating quiz: {str(e)}")

def show_study_plan_generator():
    st.header("📅 Study Plan Generator")
    
    with st.form("study_plan_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("📚 Subject", placeholder="e.g., Machine Learning Fundamentals")
            duration = st.selectbox("⏱️ Duration", ["1 hour", "2 hours", "4 hours", "1 day", "1 week", "1 month"])
            difficulty = st.selectbox("🎯 Difficulty", ["beginner", "intermediate", "advanced"])
        
        with col2:
            objectives = st.text_area("🎯 Learning Objectives", placeholder="Enter learning objectives, one per line")
            use_curation = st.checkbox("✨ Use Prompt Curation", value=True)
        
        submitted = st.form_submit_button("📅 Generate Study Plan", type="primary")
        
        if submitted and subject:
            objectives_list = [obj.strip() for obj in objectives.split('\n') if obj.strip()] if objectives else []
            
            with st.spinner(f"Creating {duration} study plan for {subject}..."):
                # Build study plan prompt
                plan_prompt = f"""Create a comprehensive {duration} study plan for {subject} at {difficulty} level.

Requirements:
- Break down into clear time blocks and sessions
- Include specific topics, concepts, and skills to learn
- Provide recommended resources and materials
- Include practice exercises and self-assessment checkpoints
- Make it actionable with concrete steps
- Format with clear headings and time allocations

Subject: {subject}
Duration: {duration}
Difficulty: {difficulty}
Learning Objectives: {', '.join(objectives_list) if objectives_list else 'General mastery of the subject'}

Create a detailed, minute-by-minute study plan that maximizes learning efficiency."""

                # Curate prompt if enabled
                if use_curation:
                    plan_prompt = curate_prompt(
                        plan_prompt,
                        "Optimize this prompt for generating effective study plans"
                    )
                
                try:
                    # Generate study plan
                    result = ollama_adapter.generate(
                        plan_prompt,
                        max_tokens=2500,
                        temperature=0.7
                    )
                    
                    if result.get('success'):
                        content = result['content']
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"study_plan_{subject.lower().replace(' ', '_')}_{timestamp}.md"
                        
                        # Save content
                        save_content(content, filename, "study_plan")
                        
                        st.success("✅ Study plan generated successfully!")
                        
                        # Display the study plan
                        st.subheader("📅 Generated Study Plan")
                        st.markdown(content)
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Study Plan",
                            data=content,
                            file_name=filename,
                            mime="text/markdown"
                        )
                        
                    else:
                        st.error(f"❌ Failed to generate study plan: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating study plan: {str(e)}")

def show_code_generator():
    st.header("💻 Code Generator")
    
    with st.form("code_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            module_name = st.text_input("📦 Module Name", value="study_utils", placeholder="e.g., data_analyzer")
            functionality = st.text_area("⚡ Functionality", placeholder="Describe what the code should do...")
        
        with col2:
            include_tests = st.checkbox("🧪 Include Unit Tests", value=True)
            use_curation = st.checkbox("✨ Use Prompt Curation", value=True)
        
        submitted = st.form_submit_button("💻 Generate Code", type="primary")
        
        if submitted and functionality:
            with st.spinner(f"Generating {module_name} module..."):
                # Build code prompt
                code_prompt = f"""Create a Python module named '{module_name}' with the following functionality:

{functionality}

Requirements:
- Write clean, well-documented Python code
- Include proper docstrings for all functions and classes
- Add type hints where appropriate
- Follow PEP 8 style guidelines
- Include error handling where needed
- Make the code modular and reusable
{'- Include comprehensive unit tests' if include_tests else ''}

Module name: {module_name}
Functionality: {functionality}

Create a complete, production-ready Python module."""

                # Curate prompt if enabled
                if use_curation:
                    code_prompt = curate_prompt(
                        code_prompt,
                        "Optimize this prompt for generating high-quality Python code"
                    )
                
                try:
                    # Generate code
                    result = ollama_adapter.generate(
                        code_prompt,
                        max_tokens=3000,
                        temperature=0.3  # Lower temperature for more precise code
                    )
                    
                    if result.get('success'):
                        content = result['content']
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{module_name}_{timestamp}.py"
                        
                        # Save content
                        save_content(content, filename, "code")
                        
                        st.success("✅ Code generated successfully!")
                        
                        # Display the code
                        st.subheader("💻 Generated Code")
                        st.code(content, language="python")
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Code",
                            data=content,
                            file_name=filename,
                            mime="text/x-python"
                        )
                        
                    else:
                        st.error(f"❌ Failed to generate code: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating code: {str(e)}")

def show_file_manager():
    st.header("📁 File Manager")
    
    if st.session_state.generated_content:
        st.subheader("📄 Generated Content")
        
        for i, item in enumerate(reversed(st.session_state.generated_content)):
            with st.expander(f"{item['type'].title()}: {item['filename']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Created:** {item['created_at']}")
                    st.write(f"**Type:** {item['type']}")
                    st.write(f"**File:** {item['filename']}")
                
                with col2:
                    st.download_button(
                        label="💾 Download",
                        data=item['content'],
                        file_name=item['filename'],
                        key=f"download_{i}"
                    )
                
                # Preview content (first 500 chars)
                preview = item['content'][:500]
                if len(item['content']) > 500:
                    preview += "..."
                
                if item['type'] == 'code':
                    st.code(preview, language="python")
                else:
                    st.markdown(preview)
    else:
        st.info("📝 No content generated yet. Use the generators to create quizzes, study plans, or code!")

def show_settings():
    st.header("⚙️ Settings")
    
    config = get_config()
    
    st.subheader("🤖 AI Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Ollama Host", value=config['ollama_host'], disabled=True)
        st.text_input("Default Model", value=config['default_model'], disabled=True)
    
    with col2:
        st.text_input("Curator Service URL", value=config['curator_url'], disabled=True)
        st.text_input("Obsidian Vault Path", value=config['vault_path'] or "Not configured", disabled=True)
    
    st.info("💡 To modify these settings, update your environment variables and restart the application.")
    
    st.subheader("🗂️ Data Management")
    
    if st.button("🗑️ Clear Generated Content"):
        st.session_state.generated_content = []
        st.success("✅ Generated content cleared!")
        st.rerun()

if __name__ == "__main__":
    main()
