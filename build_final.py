#!/usr/bin/env python3
"""
Build Final Deliverable for Academic Apex Strategist

Creates the academic_apex_final.zip package containing all necessary
components for deployment and distribution.
"""

import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime

def create_final_deliverable():
    """Create the final deliverable zip package."""
    print("🚀 Building Academic Apex Strategist Final Deliverable")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create temporary directory for staging
    with tempfile.TemporaryDirectory() as temp_dir:
        staging_dir = Path(temp_dir) / "academic_apex"
        staging_dir.mkdir()
        
        print("📁 Copying project files...")
        
        # Copy main components
        components = [
            ("backend", "Backend FastAPI service"),
            ("frontend", "React TypeScript frontend"),
            ("agentforge_academic_apex", "Executable and legacy components"),
        ]
        
        for component, description in components:
            src_path = project_root / component
            if src_path.exists():
                print(f"  ✓ {description}: {component}")
                shutil.copytree(src_path, staging_dir / component)
            else:
                print(f"  ⚠ Missing: {component}")
        
        # Copy configuration files
        config_files = [
            ("docker-compose.yml", "Docker Compose configuration"),
            ("README.md", "Main documentation"),
            ("TODO.md", "Roadmap and alternative models"),
            (".env.example", "Environment configuration template"),
        ]
        
        for file_name, description in config_files:
            src_file = project_root / file_name
            if src_file.exists():
                print(f"  ✓ {description}: {file_name}")
                shutil.copy2(src_file, staging_dir / file_name)
            else:
                print(f"  ⚠ Missing: {file_name}")
        
        # Create LICENSE if it doesn't exist
        license_file = staging_dir / "LICENSE"
        if not license_file.exists():
            print("  ✓ Creating MIT License")
            license_content = """MIT License

Copyright (c) 2025 Academic Apex Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
            with open(license_file, 'w') as f:
                f.write(license_content)
        
        # Create installation scripts
        print("  ✓ Creating installation scripts")
        
        # Windows installation script
        windows_script = staging_dir / "install_windows.bat"
        with open(windows_script, 'w') as f:
            f.write("""@echo off
echo Academic Apex Strategist - Windows Installation
echo =============================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.11+ first.
    pause
    exit /b 1
)

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
npm install
cd ..

echo Installation complete!
echo.
echo Quick Start:
echo 1. Install and start Ollama with a model (e.g., ollama pull mistral:7b)
echo 2. Run: python agentforge_academic_apex/main_launcher.py
echo 3. Open http://localhost:5000 in your browser
echo.
pause
""")
        
        # Linux/macOS installation script
        unix_script = staging_dir / "install.sh"
        with open(unix_script, 'w') as f:
            f.write("""#!/bin/bash
echo "Academic Apex Strategist - Unix Installation"
echo "============================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.11+ first."
    exit 1
fi

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
python3 -m pip install -r requirements.txt
cd ..

# Install frontend dependencies (if Node.js available)
if command -v npm &> /dev/null; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "WARNING: Node.js/npm not found. Frontend development will not be available."
    echo "For production use, this is not required."
fi

echo "Installation complete!"
echo
echo "Quick Start:"
echo "1. Install and start Ollama with a model (e.g., ollama pull mistral:7b)"
echo "2. Run: python3 agentforge_academic_apex/main_launcher.py"
echo "3. Open http://localhost:5000 in your browser"
echo
""")
        
        # Make Unix script executable
        os.chmod(unix_script, 0o755)
        
        # Create deployment guide
        print("  ✓ Creating deployment guide")
        
        deployment_guide = staging_dir / "DEPLOYMENT.md"
        with open(deployment_guide, 'w', encoding='utf-8') as f:
            f.write("""# Academic Apex Strategist - Deployment Guide

## Quick Start

### Option 1: Executable (Recommended for Users)
1. Navigate to `agentforge_academic_apex/`
2. Run `python main_launcher.py`
3. Access the application at http://localhost:5000

### Option 2: Docker Deployment (Recommended for Production)
1. Ensure Docker and Docker Compose are installed
2. Copy `.env.example` to `.env` and configure
3. Run: `docker-compose up -d`
4. Access the application at http://localhost:3000

### Option 3: Development Setup
1. Run installation script for your platform:
   - Windows: `install_windows.bat`
   - Unix/macOS: `./install.sh`
2. Start backend: `cd backend && uvicorn main:app --reload`
3. Start frontend: `cd frontend && npm run dev`
4. Start curator (optional): `cd agentforge_academic_apex && python curator_service.py`

## Prerequisites

### Required
- **Ollama**: Download from https://ollama.ai and install
- **Models**: Run `ollama pull mistral:7b` (or your preferred model)
- **Python**: 3.11 or higher
- **System**: 8GB RAM minimum, 16GB recommended

### Optional (for development)
- **Node.js**: 18.x or higher for frontend development
- **Docker**: For containerized deployment
- **Tesseract OCR**: For document processing features

## Configuration

### Environment Variables
Create a `.env` file with your configuration:

```bash
# Core Configuration
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=mistral:7b
CURATOR_MODEL=mistral:7b

# Services
CURATOR_SERVICE_URL=http://localhost:5001
WEB_UI_PORT=5000

# Obsidian Integration (Optional)
OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault

# File Storage
UPLOAD_DIR=./uploads
GENERATED_DIR=./generated
```

### Ollama Setup
```bash
# Install Ollama (see https://ollama.ai for platform-specific instructions)
ollama pull mistral:7b
ollama serve
```

## Troubleshooting

### Common Issues

**"Connection failed"**
- Ensure Ollama is running: `ollama serve`
- Check the model is available: `ollama list`

**"Port already in use"**
- Change ports in your `.env` file
- Kill existing processes: `lsof -ti:5000 | xargs kill`

**"Import errors"**
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

**Performance issues**
- Use smaller models for limited hardware
- Close unnecessary applications
- Monitor system resources

## Architecture

```
Frontend (React) → Backend (FastAPI) → Ollama (Local AI)
     ↓                    ↓
File Manager         Curator Service
     ↓                    ↓
Obsidian Vault      Generated Content
```

## Support

- **Documentation**: README.md
- **Issues**: Check logs in `logs/` directory
- **Models**: See TODO.md for alternative model recommendations
- **Updates**: Check GitHub for latest releases

---

For detailed documentation, see README.md
For roadmap and alternative models, see TODO.md
""")
        
        print("📦 Creating ZIP archive...")
        
        # Create the final ZIP file
        zip_path = project_root / "academic_apex_final.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(staging_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(staging_dir)
                    zipf.write(file_path, arc_path)
                    
        print("✅ Academic Apex Strategist package created successfully!")
        print(f"📍 Location: {zip_path.absolute()}")
        print(f"📊 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n" + "=" * 60)
        print("🎉 FINAL DELIVERABLE READY!")
        print("=" * 60)
        
        return str(zip_path.absolute())

if __name__ == "__main__":
    try:
        final_path = create_final_deliverable()
        print(f"\nFinal deliverable location: {final_path}")
    except Exception as e:
        print(f"❌ Error creating deliverable: {e}")
        exit(1)
