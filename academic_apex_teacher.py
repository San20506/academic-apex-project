#!/usr/bin/env python3
"""
Academic Apex Teacher - BYJU'S Style Learning Platform
AI-powered personalized teaching system with note analysis
"""

import streamlit as st
import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
import time
import base64
from io import BytesIO

# Document processing imports
try:
    import pytesseract
    import fitz  # PyMuPDF
    from PIL import Image
    import cv2
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    from streamlit_option_menu import option_menu
    OCR_AVAILABLE = True
except ImportError as e:
    OCR_AVAILABLE = False
    st.error(f"⚠️ Missing OCR dependencies: {e}")

# Set page config with BYJU'S-inspired styling
st.set_page_config(
    page_title="Academic Apex Teacher",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for BYJU'S-style interface
st.markdown("""
<style>
    /* BYJU'S-inspired color scheme */
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #FF6B6B;
        --accent-color: #4ECDC4;
        --success-color: #51CF66;
        --warning-color: #FFD93D;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main header styling */
    .main-header {
        background: var(--background-gradient);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid var(--primary-color);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #f0f0f0;
        border-radius: 20px;
        padding: 5px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: var(--background-gradient);
        height: 20px;
        border-radius: 15px;
        transition: width 0.3s ease;
    }
    
    /* Interactive elements */
    .concept-bubble {
        background: var(--accent-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        margin: 0.25rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .concept-bubble:hover {
        transform: scale(1.05);
        background: var(--primary-color);
    }
    
    /* Learning path styling */
    .learning-step {
        background: linear-gradient(90deg, var(--success-color), var(--accent-color));
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        position: relative;
    }
    
    .learning-step::before {
        content: "✓";
        position: absolute;
        left: -15px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--success-color);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 3px dashed var(--primary-color);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(45deg, rgba(108,99,255,0.1), rgba(76,201,196,0.1));
        margin: 1rem 0;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

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
    st.session_state.uploaded_documents = []
    st.session_state.learning_progress = {}
    st.session_state.current_lesson = None
    st.session_state.extracted_concepts = []
    st.session_state.learning_path = []

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

# Document processing functions
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text() + "\n"
        pdf_document.close()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_text_from_image(image_file):
    """Extract text from image using OCR"""
    if not OCR_AVAILABLE:
        st.error("OCR functionality not available. Please install required dependencies.")
        return ""
    
    try:
        # Read image
        image = Image.open(image_file)
        
        # Convert to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Preprocessing for better OCR
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply preprocessing
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(enhanced, config='--psm 6')
        
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {str(e)}")
        return ""

def analyze_document_content(text):
    """Analyze document content and extract learning concepts"""
    if not text.strip():
        return []
    
    analysis_prompt = f"""Analyze the following educational content and extract key learning concepts, topics, and subtopics. 
    Create a structured breakdown that can be used for personalized learning.

Content:
{text[:3000]}...

Please provide:
1. Main topics/subjects covered
2. Key concepts under each topic
3. Difficulty level estimation (Beginner/Intermediate/Advanced)
4. Prerequisites needed
5. Learning objectives
6. Estimated time to master each concept

Format as JSON with clear structure for educational planning."""

    try:
        result = ollama_adapter.generate(
            analysis_prompt,
            max_tokens=2000,
            temperature=0.3
        )
        
        if result.get('success'):
            return result['content']
        else:
            return "Analysis failed"
    except Exception as e:
        st.error(f"Error analyzing document: {str(e)}")
        return "Analysis error"

def create_personalized_learning_path(concepts, user_level="intermediate"):
    """Create a personalized learning path based on extracted concepts"""
    if not concepts:
        return []
    
    path_prompt = f"""Based on the following educational concepts, create a personalized learning path for a {user_level} level student.
    
    Break down into:
    1. Daily learning modules (15-30 minutes each)
    2. Progressive difficulty
    3. Interactive exercises and checkpoints
    4. Real-world applications
    5. Assessment points
    
    Concepts to organize:
    {concepts[:2000]}
    
    Create a structured learning journey that guides the student step-by-step, similar to BYJU's teaching methodology.
    Include specific learning goals, practice exercises, and progress milestones."""

    try:
        result = ollama_adapter.generate(
            path_prompt,
            max_tokens=3000,
            temperature=0.4
        )
        
        if result.get('success'):
            return result['content']
        else:
            return "Path creation failed"
    except Exception as e:
        st.error(f"Error creating learning path: {str(e)}")
        return "Path creation error"

def generate_interactive_lesson(topic, concepts, previous_knowledge=""):
    """Generate an interactive lesson for a specific topic"""
    lesson_prompt = f"""Create an interactive, engaging lesson on "{topic}" in the style of BYJU's teaching methodology.

    Key concepts to cover: {concepts}
    Student's previous knowledge: {previous_knowledge}

    Structure the lesson with:
    1. 🎯 Learning Objective (What will you master?)
    2. 🔍 Real-world Connection (Why is this important?)
    3. 📚 Core Concept Explanation (Simple, visual explanations)
    4. 💡 Interactive Examples (Step-by-step problem solving)
    5. 🧠 Practice Questions (Progressive difficulty)
    6. ✅ Quick Assessment (Check understanding)
    7. 🚀 Next Steps (What comes next?)

    Make it engaging, use analogies, and include opportunities for interaction.
    Use emojis and formatting to make it visually appealing.
    Include specific questions for the student to answer."""

    try:
        result = ollama_adapter.generate(
            lesson_prompt,
            max_tokens=3500,
            temperature=0.6
        )
        
        if result.get('success'):
            return result['content']
        else:
            return "Lesson generation failed"
    except Exception as e:
        st.error(f"Error generating lesson: {str(e)}")
        return "Lesson generation error"

# Main App Layout
def main():
    # Header with BYJU'S-style branding
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🎓 Academic Apex Teacher</h1>
        <p>Your AI-Powered Personal Learning Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["🏠 Dashboard", "📚 Upload Notes", "🎯 Learn", "📊 Progress", "🧪 Practice", "⚙️ Settings"],
        icons=['house', 'upload', 'book', 'graph-up', 'flask', 'gear'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#6C63FF", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#6C63FF"},
        }
    )
    
    # Route to different pages
    if selected == "🏠 Dashboard":
        show_dashboard()
    elif selected == "📚 Upload Notes":
        show_upload_notes()
    elif selected == "🎯 Learn":
        show_learning_interface()
    elif selected == "📊 Progress":
        show_progress_tracking()
    elif selected == "🧪 Practice":
        show_practice_zone()
    elif selected == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """BYJU'S-style dashboard with learning overview"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Documents</h3>
            <h2>{}</h2>
            <p>Notes Uploaded</p>
        </div>
        """.format(len(st.session_state.uploaded_documents)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Concepts</h3>
            <h2>{}</h2>
            <p>Topics Identified</p>
        </div>
        """.format(len(st.session_state.extracted_concepts)), unsafe_allow_html=True)
    
    with col3:
        progress = len(st.session_state.learning_progress)
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Progress</h3>
            <h2>{}%</h2>
            <p>Completion Rate</p>
        </div>
        """.format(progress * 10 if progress < 10 else 100), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>⭐ Streak</h3>
            <h2>0</h2>
            <p>Days Learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Start Section
    st.markdown("### 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(st.session_state.uploaded_documents) == 0:
            if st.button("📚 Upload Your First Notes", type="primary", use_container_width=True):
                st.switch_page("📚 Upload Notes")
        else:
            if st.button("🎯 Continue Learning", type="primary", use_container_width=True):
                st.switch_page("🎯 Learn")
    
    with col2:
        if len(st.session_state.extracted_concepts) > 0:
            if st.button("🧪 Take Practice Quiz", use_container_width=True):
                st.switch_page("🧪 Practice")
    
    # Recent Activity
    if len(st.session_state.uploaded_documents) > 0:
        st.markdown("### 📋 Recent Activity")
        
        for doc in st.session_state.uploaded_documents[-3:]:
            st.markdown(f"""
            <div class="feature-card">
                <h4>📄 {doc['name']}</h4>
                <p>Uploaded: {doc['uploaded_at']}</p>
                <p>Type: {doc['type']} | Size: {doc.get('size', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)

def show_upload_notes():
    """Enhanced note upload with OCR and analysis"""
    
    st.markdown("### 📚 Upload Your Learning Materials")
    
    st.markdown("""
    <div class="upload-area">
        <h3>🎯 Supported Formats</h3>
        <p>📄 PDF Files • 🖼️ Images (JPG, PNG) • 📝 Text Files</p>
        <p><strong>Including handwritten notes!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose your files",
        accept_multiple_files=True,
        type=['pdf', 'txt', 'jpg', 'jpeg', 'png', 'bmp', 'tiff']
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown(f"**Processing:** {uploaded_file.name}")
            
            with st.spinner(f"Analyzing {uploaded_file.name}..."):
                # Determine file type and extract text
                file_extension = uploaded_file.name.split('.')[-1].lower()
                extracted_text = ""
                
                if file_extension == 'pdf':
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
                    extracted_text = extract_text_from_image(uploaded_file)
                elif file_extension == 'txt':
                    extracted_text = str(uploaded_file.read(), "utf-8")
                
                if extracted_text:
                    # Analyze content
                    concepts = analyze_document_content(extracted_text)
                    
                    # Store document info
                    doc_info = {
                        'name': uploaded_file.name,
                        'type': file_extension.upper(),
                        'size': f"{len(uploaded_file.getvalue())} bytes",
                        'uploaded_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'text': extracted_text,
                        'concepts': concepts
                    }
                    
                    st.session_state.uploaded_documents.append(doc_info)
                    st.session_state.extracted_concepts.append(concepts)
                    
                    # Show preview
                    st.success(f"✅ Successfully processed {uploaded_file.name}")
                    
                    with st.expander(f"📄 Preview: {uploaded_file.name}"):
                        st.markdown("**Extracted Text (first 500 characters):**")
                        st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
                        
                        st.markdown("**Identified Concepts:**")
                        st.text(concepts[:500] + "..." if len(str(concepts)) > 500 else str(concepts))
                
                else:
                    st.error(f"❌ Could not extract text from {uploaded_file.name}")
        
        # Generate learning path button
        if len(st.session_state.uploaded_documents) > 0:
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                user_level = st.selectbox(
                    "📊 Your current level:",
                    ["beginner", "intermediate", "advanced"]
                )
            
            with col2:
                if st.button("🎯 Create My Learning Path", type="primary", use_container_width=True):
                    with st.spinner("Creating your personalized learning journey..."):
                        all_concepts = "\n".join([str(concept) for concept in st.session_state.extracted_concepts])
                        learning_path = create_personalized_learning_path(all_concepts, user_level)
                        st.session_state.learning_path = learning_path
                        
                        st.success("🎉 Your personalized learning path is ready!")
                        st.markdown("### 🗺️ Your Learning Journey")
                        st.markdown(learning_path)

def show_learning_interface():
    """Interactive learning interface similar to BYJU's"""
    
    if len(st.session_state.uploaded_documents) == 0:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 No Notes Uploaded Yet</h3>
            <p>Upload your notes to start your personalized learning journey!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Upload Notes", type="primary"):
            st.switch_page("📚 Upload Notes")
        return
    
    st.markdown("### 🎯 Your Learning Session")
    
    # Topic selection
    topics = []
    for doc in st.session_state.uploaded_documents:
        if doc['concepts']:
            topics.append(f"📄 {doc['name']}")
    
    if topics:
        selected_topic = st.selectbox("Choose what to learn:", topics)
        
        if selected_topic:
            # Get the selected document
            doc_name = selected_topic.replace("📄 ", "")
            selected_doc = next((doc for doc in st.session_state.uploaded_documents if doc['name'] == doc_name), None)
            
            if selected_doc:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if st.button("🚀 Start Learning Session", type="primary", use_container_width=True):
                        with st.spinner("Preparing your personalized lesson..."):
                            lesson = generate_interactive_lesson(
                                selected_doc['name'],
                                selected_doc['concepts'],
                                "Intermediate level student"
                            )
                            st.session_state.current_lesson = lesson
                
                with col2:
                    st.markdown("**📊 Session Info**")
                    st.markdown(f"📚 Topic: {doc_name}")
                    st.markdown(f"⏱️ Est. Time: 20-30 min")
                    st.markdown(f"🎯 Level: Adaptive")
                
                # Display current lesson
                if st.session_state.current_lesson:
                    st.markdown("---")
                    st.markdown("### 📖 Your Lesson")
                    
                    st.markdown(f"""
                    <div class="feature-card fade-in">
                        {st.session_state.current_lesson}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Interactive elements
                    st.markdown("---")
                    st.markdown("### 💬 Interactive Practice")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        user_answer = st.text_area(
                            "✍️ Your answer to the practice question:",
                            height=100
                        )
                        
                        if st.button("📝 Submit Answer"):
                            if user_answer:
                                # Process answer with AI
                                feedback_prompt = f"""
                                Evaluate this student's answer and provide constructive feedback:
                                
                                Question context: {selected_doc['concepts'][:500]}
                                Student's answer: {user_answer}
                                
                                Provide:
                                1. What they got right
                                2. Areas for improvement
                                3. Hints for better understanding
                                4. Next steps
                                
                                Be encouraging and educational like BYJU's teaching style.
                                """
                                
                                try:
                                    feedback_result = ollama_adapter.generate(
                                        feedback_prompt,
                                        max_tokens=1500,
                                        temperature=0.7
                                    )
                                    
                                    if feedback_result.get('success'):
                                        st.success("✅ Answer submitted!")
                                        st.markdown("**🎯 Personalized Feedback:**")
                                        st.markdown(feedback_result['content'])
                                        
                                        # Update progress
                                        if selected_doc['name'] not in st.session_state.learning_progress:
                                            st.session_state.learning_progress[selected_doc['name']] = 0
                                        st.session_state.learning_progress[selected_doc['name']] += 10
                                        
                                except Exception as e:
                                    st.error(f"Error processing answer: {str(e)}")
                            else:
                                st.warning("Please provide an answer first!")
                    
                    with col2:
                        st.markdown("**🎯 Learning Tips**")
                        st.info("💡 Don't worry about being perfect! Learning is about progress, not perfection.")
                        st.info("🔄 Try to explain concepts in your own words")
                        st.info("❓ Ask questions when something isn't clear")
                        
                        # Progress for this topic
                        progress = st.session_state.learning_progress.get(selected_doc['name'], 0)
                        st.markdown(f"**📈 Progress: {progress}%**")
                        st.progress(progress / 100)

def show_progress_tracking():
    """BYJU'S-style progress tracking with visual analytics"""
    
    st.markdown("### 📊 Your Learning Analytics")
    
    if len(st.session_state.learning_progress) == 0:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Start Learning to See Progress</h3>
            <p>Complete lessons and practice sessions to track your improvement!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Overall progress
    overall_progress = sum(st.session_state.learning_progress.values()) / len(st.session_state.learning_progress)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Overall Progress", f"{overall_progress:.1f}%", f"+{overall_progress/10:.1f}")
    
    with col2:
        st.metric("📚 Topics Studied", len(st.session_state.learning_progress))
    
    with col3:
        completed = sum(1 for progress in st.session_state.learning_progress.values() if progress >= 80)
        st.metric("✅ Topics Mastered", completed)
    
    # Progress chart
    if st.session_state.learning_progress:
        st.markdown("### 📈 Progress by Topic")
        
        topics = list(st.session_state.learning_progress.keys())
        progress_values = list(st.session_state.learning_progress.values())
        
        fig = go.Figure(data=[
            go.Bar(x=topics, y=progress_values, 
                   marker_color='rgba(108, 99, 255, 0.8)')
        ])
        
        fig.update_layout(
            title="Learning Progress by Topic",
            xaxis_title="Topics",
            yaxis_title="Progress (%)",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed progress
    st.markdown("### 📋 Detailed Progress")
    
    for topic, progress in st.session_state.learning_progress.items():
        st.markdown(f"""
        <div class="feature-card">
            <h4>📚 {topic}</h4>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
            <p>{progress}% Complete</p>
        </div>
        """, unsafe_allow_html=True)

def show_practice_zone():
    """Interactive practice and assessment zone"""
    
    st.markdown("### 🧪 Practice Zone")
    
    if len(st.session_state.uploaded_documents) == 0:
        st.markdown("""
        <div class="feature-card">
            <h3>🧪 No Practice Available Yet</h3>
            <p>Upload your notes first to generate personalized practice questions!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Practice options
    practice_type = st.selectbox(
        "Choose practice type:",
        ["🧠 Quick Quiz", "📝 Concept Review", "🎯 Targeted Practice", "🏆 Challenge Mode"]
    )
    
    if practice_type == "🧠 Quick Quiz":
        show_quick_quiz()
    elif practice_type == "📝 Concept Review":
        show_concept_review()
    elif practice_type == "🎯 Targeted Practice":
        show_targeted_practice()
    elif practice_type == "🏆 Challenge Mode":
        show_challenge_mode()

def show_quick_quiz():
    """Generate and display a quick quiz"""
    
    st.markdown("#### 🧠 Quick Quiz")
    
    # Select topic for quiz
    topics = [doc['name'] for doc in st.session_state.uploaded_documents]
    selected_topic = st.selectbox("Select topic for quiz:", topics)
    
    if selected_topic and st.button("🎯 Generate Quiz", type="primary"):
        selected_doc = next((doc for doc in st.session_state.uploaded_documents if doc['name'] == selected_topic), None)
        
        if selected_doc:
            with st.spinner("Creating your personalized quiz..."):
                quiz_prompt = f"""
                Create a 5-question quiz based on these concepts:
                
                {selected_doc['concepts'][:1500]}
                
                Make it:
                1. Multiple choice with 4 options each
                2. Progressive difficulty
                3. Include explanations for correct answers
                4. Engaging and educational
                
                Format clearly with questions, options, and answer explanations.
                """
                
                try:
                    quiz_result = ollama_adapter.generate(
                        quiz_prompt,
                        max_tokens=2500,
                        temperature=0.4
                    )
                    
                    if quiz_result.get('success'):
                        st.markdown("### 📝 Your Quiz")
                        st.markdown(quiz_result['content'])
                        
                        # Quiz interaction
                        st.markdown("---")
                        user_answers = st.text_area("📝 Your answers (e.g., 1:A, 2:B, 3:C, 4:D, 5:A):")
                        
                        if st.button("✅ Submit Quiz") and user_answers:
                            st.success("🎉 Quiz submitted! Great job practicing!")
                            
                            # Update progress
                            if selected_topic not in st.session_state.learning_progress:
                                st.session_state.learning_progress[selected_topic] = 0
                            st.session_state.learning_progress[selected_topic] += 15
                        
                except Exception as e:
                    st.error(f"Error generating quiz: {str(e)}")

def show_concept_review():
    """Interactive concept review"""
    st.markdown("#### 📝 Concept Review")
    st.info("💡 Review key concepts with spaced repetition for better retention!")

def show_targeted_practice():
    """Targeted practice for weak areas"""
    st.markdown("#### 🎯 Targeted Practice")
    st.info("🎯 Focus on areas that need improvement based on your progress!")

def show_challenge_mode():
    """Advanced challenge mode"""
    st.markdown("#### 🏆 Challenge Mode")
    st.info("🏆 Ready for advanced challenges? Test your mastery!")

def show_settings():
    """Settings and configuration"""
    
    st.markdown("### ⚙️ Settings")
    
    config = get_config()
    
    st.markdown("#### 🤖 AI Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Ollama Host", value=config['ollama_host'], disabled=True)
        st.text_input("Default Model", value=config['default_model'], disabled=True)
    
    with col2:
        st.text_input("Curator Service URL", value=config['curator_url'], disabled=True)
        st.text_input("Obsidian Vault Path", value=config['vault_path'] or "Not configured", disabled=True)
    
    st.markdown("#### 🎓 Learning Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        learning_style = st.selectbox(
            "Preferred learning style:",
            ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
        )
        
        difficulty_preference = st.selectbox(
            "Difficulty preference:",
            ["Start Easy", "Balanced", "Challenge Me"]
        )
    
    with col2:
        session_length = st.selectbox(
            "Preferred session length:",
            ["15 minutes", "30 minutes", "45 minutes", "1 hour"]
        )
        
        reminder_frequency = st.selectbox(
            "Study reminders:",
            ["Daily", "Every other day", "Weekly", "Off"]
        )
    
    st.markdown("#### 🗂️ Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Progress"):
            st.session_state.learning_progress = {}
            st.success("✅ Progress cleared!")
    
    with col2:
        if st.button("📄 Export Learning Data"):
            st.info("💾 Export functionality coming soon!")

if __name__ == "__main__":
    main()
