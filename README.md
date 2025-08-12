# 🎓 Academic Apex Teacher

**AI-Powered Personal Learning Platform inspired by BYJU'S**

Transform your handwritten and typed notes into personalized, interactive learning experiences using local AI models.

## ✨ Features

- **📚 Smart Note Upload** - PDF, images, handwritten notes with OCR
- **🤖 AI Teaching** - Personalized lessons in BYJU'S style  
- **📊 Progress Tracking** - Visual analytics and learning paths
- **🧪 Interactive Practice** - Quizzes and concept reviews
- **🎨 Beautiful UI** - Modern interface with gradients and animations
- **🔒 Privacy-First** - Everything runs locally with Ollama

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR (for handwritten notes)
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

### 3. Start Ollama
```bash
ollama serve
ollama pull mistral:7b
```

### 4. Run the App
```bash
streamlit run academic_apex_teacher.py
```

### 5. Open in Browser
Visit: `http://localhost:8501`

## 📱 How to Use

1. **Upload Notes** - PDF files, images of handwritten notes, or text files
2. **AI Analysis** - Watch as AI extracts concepts and creates learning paths  
3. **Start Learning** - Interactive lessons with step-by-step explanations
4. **Practice & Track** - Take quizzes and monitor your progress
5. **Get Feedback** - Receive personalized AI feedback on your answers

## 🌐 Deploy to Cloud

### Streamlit Cloud (FREE)
1. Push to GitHub: `git push origin main`
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy with `academic_apex_teacher.py`

## 📋 Files

- `academic_apex_teacher.py` - Main BYJU'S-style application
- `ollama_adapter.py` - AI model interface
- `obsidian_adapter.py` - Note management (optional)
- `requirements.txt` - Python dependencies
- `DEPLOYMENT_GUIDE.md` - Detailed deployment instructions

## 🎯 BYJU'S-Style Features

- **Bite-sized Learning** - 15-30 minute focused sessions
- **Interactive Explanations** - Step-by-step with real-world examples
- **Adaptive Difficulty** - Adjusts based on your progress  
- **Visual Progress** - Charts and streak tracking
- **Personalized Feedback** - AI evaluates your answers

## 💡 Tips for Best Results

- **Clear Images**: Use good lighting for handwritten notes
- **Engage Actively**: Answer practice questions in the lessons
- **Regular Practice**: Take quizzes to reinforce learning
- **Track Progress**: Review analytics to identify weak areas

## 🔧 Troubleshooting

**OCR not working?**
- Install Tesseract OCR for your operating system
- Ensure images are clear and well-lit

**AI responses slow?**  
- Check that Ollama is running: `ollama serve`
- Try smaller models if your system is limited

**Deployment issues?**
- Verify all requirements are installed
- Check that environment variables are set correctly

## 🤝 Contributing

Feel free to contribute improvements, bug fixes, or new features!

1. Fork the repository
2. Create a feature branch
3. Make your changes  
4. Submit a pull request

## 📄 License

MIT License - feel free to use for educational purposes!

---

**Transform your notes into a complete learning experience with AI! 🎓✨**
