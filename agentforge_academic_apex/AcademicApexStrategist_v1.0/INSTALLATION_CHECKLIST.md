# 📋 Installation Checklist 
 
## ✅ Prerequisites 
 
- [ ] Windows 10/11 (64-bit) 
- [ ] **Ollama installed** from [ollama.ai](https://ollama.ai/download) 
- [ ] **AI models installed**: 
  - [ ] `ollama pull mistral-7b` 
  - [ ] `ollama pull deepseek-coder` (optional) 
 
## 🚀 Quick Start 
 
1. **Extract** this folder anywhere on your computer 
2. **Run** `setup_environment.bat` (optional - for Obsidian integration) 
3. **Start Ollama**: Open cmd and run `ollama serve` 
4. **Run Academic Apex**: Double-click `Run_AcademicApex.bat` 
5. **Open browser** to: http://localhost:5000 
 
## 🔧 Troubleshooting 
 
**Executable won't start?** 
- Run from command line: `AcademicApexStrategist.exe` 
- Check if Ollama is running: `ollama list` 
 
**Port conflicts?** 
- Set different port: `set WEB_UI_PORT=5001` 
 
**Need help?** 
- Read the full `README.md` 
- Check system status on the dashboard 
