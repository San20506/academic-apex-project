# 🚀 Quick Start Guide

Get Academic Apex Strategist running in just a few minutes!

## ✅ Prerequisites

1. **Python 3.10+**: Download from [python.org](https://python.org)
2. **Ollama**: Download from [ollama.ai](https://ollama.ai/download)
3. **Obsidian** (optional): Download from [obsidian.md](https://obsidian.md)

## 📦 Setup Steps

### 1. Install Ollama and Models

```bash
# Install required models
ollama pull deepseek-coder
ollama pull mistral-7b

# Verify installation
ollama list
```

### 2. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:OBSIDIAN_VAULT_PATH="C:\Users\YourName\Documents\MyVault"
```

**macOS/Linux:**
```bash
export OBSIDIAN_VAULT_PATH="/Users/yourname/Documents/MyVault"
```

### 3. Start Academic Apex

**Windows:**
```cmd
# Double-click start_academic_apex.bat
# OR run in terminal:
.\start_academic_apex.bat
```

**macOS/Linux:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start curator service (in background)
python curator_service.py &

# Start web interface
python web_ui.py
```

### 4. Open Web Interface

Visit: http://localhost:5000

## 🎯 First Steps

1. **Check System Status**: Look at the status indicator in the top navigation
2. **Generate a Quiz**: Click "Generate Quiz" and try "Python Programming Basics"
3. **Create Study Plan**: Make a 2-hour plan for any subject you're interested in
4. **View Your Files**: All generated content appears in the "My Files" section

## 🔧 If Something Goes Wrong

### Ollama Issues
- **Not starting?** Run `ollama serve` manually
- **Models missing?** Run `ollama pull deepseek-coder`
- **Port conflict?** Change `OLLAMA_HOST` environment variable

### Curator Service Issues
- **Won't start?** Check if port 5001 is available
- **Errors?** Run `python curator_service.py` directly to see logs

### Web UI Issues
- **Can't connect?** Try a different port with `WEB_UI_PORT=5001 python web_ui.py`
- **Permission errors?** Check if `OBSIDIAN_VAULT_PATH` directory exists and is writable

## 💡 Tips for Best Results

- **Be specific** in your quiz/study plan subjects
- **Use prompt curation** (enabled by default) for better results  
- **Set learning objectives** when creating study plans
- **Review generated content** before using with students

## 🆘 Need Help?

1. Check the **Settings** page for configuration details
2. Look at the **troubleshooting** section in Settings
3. Ensure all services show "green" status in the dashboard

---

**🎉 You're ready to create amazing educational content with AI!**
