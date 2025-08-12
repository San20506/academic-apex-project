# 📦 Academic Apex Strategist - Standalone Executable

**A complete, self-contained Windows executable for creating AI-powered educational content**

## 🚀 Quick Start

1. **Download** `AcademicApexStrategist.exe` 
2. **Install Ollama** from [ollama.ai](https://ollama.ai/download)
3. **Install AI models**:
   ```cmd
   ollama pull mistral-7b
   ollama pull deepseek-coder
   ```
4. **Run** the executable by double-clicking or from command line:
   ```cmd
   AcademicApexStrategist.exe
   ```
5. **Open browser** to: http://localhost:5000

## ✨ What's Included

This single executable contains everything you need:

- ✅ **Complete Web Interface** - Modern, responsive dashboard
- ✅ **Quiz Generator** - Create educational quizzes with AI
- ✅ **Study Plan Creator** - Generate detailed, time-blocked study plans  
- ✅ **Code Generator** - Create Python educational modules
- ✅ **File Management** - View, download, and manage generated content
- ✅ **Prompt Curation** - AI-powered prompt enhancement service
- ✅ **Obsidian Integration** - Auto-save to your knowledge vault
- ✅ **System Monitoring** - Real-time status of all services

## 🔧 Requirements

### Required:
- **Windows 10/11** (64-bit)
- **Ollama** installed and running
- **AI Models**: `mistral-7b` (minimum), `deepseek-coder` (recommended)

### Optional:
- **Obsidian** for note-taking integration
- **Git** for version control of generated content

## 📋 Environment Variables (Optional)

You can customize the executable by setting these environment variables before running:

```cmd
set OLLAMA_HOST=http://localhost:11434
set WEB_UI_PORT=5000
set CURATOR_MODEL=mistral-7b
set OBSIDIAN_VAULT_PATH=C:\Users\YourName\Documents\MyVault
set DEBUG=false
```

## 🎯 Features Overview

### **Quiz Generator**
- Create quizzes for any subject at any difficulty level
- Multiple question types (multiple choice, short answer, essay)
- Customizable number of questions (1-50)
- Automatic answer key generation
- Export to Markdown format

### **Study Plan Generator** 
- Time-blocked study sessions (30 minutes to 8 hours)
- Adaptive difficulty levels (beginner to advanced)
- Custom learning objectives
- Progress tracking and checkpoints
- Built-in study timer

### **Code Generator**
- Generate educational Python modules
- Complete with documentation and type hints
- Automatic syntax validation
- Unit test generation
- Educational best practices

### **File Management**
- View all generated content in one place
- Download files individually
- Preview files inline
- Automatic timestamping
- Search and filter capabilities

## 🔥 Advanced Features

### **Prompt Curation Service**
The executable includes an AI-powered prompt curation service that:
- Refines prompts for better AI responses
- Optimizes for educational content
- Improves clarity and specificity
- Runs automatically in the background

### **Obsidian Integration** 
If you have Obsidian installed:
- Set `OBSIDIAN_VAULT_PATH` environment variable
- Generated content automatically saved as notes
- Proper linking and tagging
- Maintains your knowledge graph

### **System Health Monitoring**
- Real-time status indicators
- Automatic service health checks
- Connection testing for all components
- Troubleshooting guidance

## 🛠️ Troubleshooting

### Executable Won't Start
```cmd
# Run from command line to see error messages
AcademicApexStrategist.exe

# Check if required services are running
ollama list
```

### Ollama Connection Issues
```cmd
# Start Ollama manually
ollama serve

# Test connection
curl http://localhost:11434/api/version
```

### Port Conflicts
```cmd
# Use different port
set WEB_UI_PORT=5001
AcademicApexStrategist.exe
```

### Generation Quality Issues
- Install additional models: `ollama pull llama2`
- Enable prompt curation (default: enabled)
- Use more specific subject descriptions
- Adjust difficulty levels appropriately

## 📁 Generated Files

All generated content is saved to:
- **Local**: `generated/` folder (next to executable)
- **Obsidian**: Your vault's designated folder (if configured)

File naming convention:
- Quizzes: `quiz_[subject]_[timestamp].md`
- Study Plans: `study_plan_[subject]_[timestamp].md` 
- Code: `[module_name]_[timestamp].py`

## 🔐 Security & Privacy

- **All processing is local** - no data sent to external services
- **No internet required** (except for Ollama model downloads)
- **Complete data control** - all files saved locally
- **No telemetry or tracking** - your content stays private

## 🆘 Support

### Getting Help
1. Check the **Settings** page for configuration details
2. Review **System Status** on the dashboard
3. Ensure all services show "green" status
4. Verify Ollama models are installed: `ollama list`

### Common Solutions
- **Restart** Ollama service: `ollama serve`
- **Reinstall** missing models: `ollama pull mistral-7b`
- **Check** environment variables are set correctly
- **Run** executable from command line to see error messages

### Performance Tips
- Use SSD storage for better response times
- Close unnecessary applications during generation
- Install models on local storage (not network drives)
- Use specific, clear prompts for better results

---

## 📋 Version Information

- **Version**: 1.0
- **Build Date**: December 2025
- **Python Version**: 3.10+
- **License**: MIT License

**🎉 Enjoy creating amazing educational content with AI!**
