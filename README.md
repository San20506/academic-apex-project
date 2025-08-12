# Academic Apex Strategist

> AI-powered educational content generation platform with local-first privacy

Academic Apex Strategist is a comprehensive educational platform that leverages local AI models to generate study plans, quizzes, code modules, and other educational content. Built with privacy-first principles, all processing happens locally without sending data to external services.

## 🚀 Features

### Core Functionality
- **📝 Quiz Generation**: Create comprehensive diagnostic quizzes for any subject
- **📅 Study Plan Generator**: Generate detailed, minute-by-minute study plans  
- **🐍 Code Generation**: Create Python modules and utilities for academic tasks
- **📄 Document Processing**: OCR and text extraction from PDFs and images
- **📁 File Management**: Organize and manage all generated content

### AI & Integration
- **🤖 Local AI Models**: Uses Ollama for completely local inference
- **✨ Prompt Curation**: Optional curator service for enhanced prompt optimization
- **📝 Obsidian Integration**: Automatic note saving to Obsidian vaults
- **🔒 Privacy-First**: No data leaves your machine unless explicitly configured

### Technical Stack
- **Backend**: FastAPI with Python 3.11+
- **Frontend**: React 18 with TypeScript and Tailwind CSS
- **AI**: Ollama integration with Mistral models (configurable)
- **Infrastructure**: Docker Compose for easy deployment
- **Storage**: Local file system with optional Obsidian sync

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Memory**: 8GB RAM minimum (16GB recommended for larger models)
- **Disk**: 10GB free space (more for model storage)
- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher (for frontend development)
- **Docker**: Optional, for containerized deployment

### Dependencies
- **Ollama**: For local AI model inference
- **Tesseract OCR**: For document text extraction (optional)
- **PyMuPDF**: For PDF processing (optional)

## 🛠️ Installation

### Method 1: Quick Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/academic-apex/academic-apex-project.git
   cd academic-apex-project
   ```

2. **Install and start Ollama**
   ```bash
   # Install Ollama (see https://ollama.ai)
   ollama pull mistral:7b
   ollama serve
   ```

3. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --reload --port 8000
   ```

4. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Start the curator service** (optional)
   ```bash
   cd agentforge_academic_apex
   python curator_service.py
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Method 2: Docker Deployment

1. **Clone and configure**
   ```bash
   git clone https://github.com/academic-apex/academic-apex-project.git
   cd academic-apex-project
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Ensure Ollama is running locally**
   ```bash
   ollama pull mistral:7b
   ollama serve
   ```

### Method 3: Executable Package

Use the pre-built executable from the `agentforge_academic_apex` directory:

```bash
# Windows
cd agentforge_academic_apex
academic_apex.exe

# Or run the Python launcher
python main_launcher.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# AI Model Configuration
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=mistral:7b
CURATOR_MODEL=mistral:7b

# Service URLs
CURATOR_SERVICE_URL=http://localhost:5001

# Obsidian Integration
OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault

# File Storage
UPLOAD_DIR=./uploads
GENERATED_DIR=./generated

# Development
DEBUG=false
WEB_UI_PORT=3000
API_PORT=8000
```

### Ollama Models

Recommended models (choose based on your hardware):

```bash
# Lightweight (4GB RAM)
ollama pull mistral:7b

# Balanced (8GB RAM)
ollama pull llama2:13b

# High-quality (16GB+ RAM)
ollama pull codellama:34b
```

### Obsidian Integration

1. Install Obsidian and create a vault
2. Set `OBSIDIAN_VAULT_PATH` to your vault directory
3. Generated content will automatically appear in `AcademicApex/` folders

## 🎯 Usage

### Quick Start Guide

1. **Ensure system health**: Check the dashboard for green status indicators
2. **Generate your first quiz**:
   - Navigate to "Generate Quiz"
   - Enter a subject (e.g., "Python Programming Basics")
   - Select difficulty and number of questions
   - Click "Generate"
3. **Create a study plan**:
   - Go to "Study Plan" 
   - Specify subject and duration
   - Add learning objectives
   - Generate your personalized plan
4. **Manage your content**: Use "File Manager" to view, download, or organize generated files

### Advanced Features

#### Document Upload & Processing
```bash
# Upload and process documents via API
curl -X POST "http://localhost:8000/api/upload-document" \
  -F "file=@document.pdf"
```

#### Prompt Curation
Enable the curator service for enhanced prompt optimization:
- Better question quality
- More focused content generation
- Improved educational value

#### Obsidian Workflow
1. Generate content in Academic Apex
2. Content automatically syncs to Obsidian
3. Use Obsidian's linking and organization features
4. Build your personal knowledge base

## 🧪 Testing

### Run Smoke Tests
```bash
cd agentforge_academic_apex
python smoke_tests.py
```

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Test the full pipeline
python -m pytest tests/integration/
```

## 🐛 Troubleshooting

### Common Issues

**❌ "Ollama connection failed"**
- Ensure Ollama is running: `ollama serve`
- Check the model is downloaded: `ollama list`
- Verify the host URL in your configuration

**❌ "Curator service offline"**
- Start the curator: `python curator_service.py`
- Check port 5001 is available
- Verify Ollama connectivity

**❌ "Obsidian vault issues"**
- Ensure the vault path exists and is writable
- Check permissions on the vault directory
- Verify the path in your environment variables

**❌ "OCR processing failed"**
- Install Tesseract: `apt-get install tesseract-ocr` (Linux) or `brew install tesseract` (macOS)
- For Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

**❌ "Slow generation times"**
- Use smaller models (e.g., mistral:7b instead of llama2:70b)
- Reduce max_tokens in requests
- Ensure sufficient RAM and CPU resources

### Performance Optimization

1. **Model Selection**: Choose models appropriate for your hardware
2. **Token Limits**: Reduce max_tokens for faster generation
3. **Caching**: Enable prompt caching in the curator service
4. **Hardware**: Use GPU acceleration if available

### Debug Mode

Enable debug mode for detailed logging:
```bash
DEBUG=true python main_launcher.py
```

## 🏗️ Architecture

### System Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │────│  FastAPI Backend│────│     Ollama      │
│   (Port 3000)   │    │   (Port 8000)   │    │  (Port 11434)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │              ┌─────────────────┐
         │              │ Curator Service │
         └──────────────│   (Port 5001)   │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │ Obsidian Vault  │
                        │  (File System)  │
                        └─────────────────┘
```

### Component Responsibilities

- **Frontend**: React SPA with TypeScript, handles UI/UX
- **Backend**: FastAPI service, manages API endpoints and business logic
- **Curator**: Flask service for prompt optimization and curation
- **Ollama**: Local AI inference engine
- **File System**: Local storage for generated content and uploads

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `npm test && pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript**: Follow ESLint rules, use Prettier for formatting
- **Commits**: Use conventional commits format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** for providing excellent local AI inference
- **Mistral AI** for the foundational language models
- **React & FastAPI** communities for excellent frameworks
- **Obsidian** for inspiring knowledge management integration

## 🔗 Links

- **Documentation**: [docs.academic-apex.dev](https://docs.academic-apex.dev)
- **Issues**: [GitHub Issues](https://github.com/academic-apex/academic-apex-project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/academic-apex/academic-apex-project/discussions)
- **Roadmap**: [Project Roadmap](https://github.com/academic-apex/academic-apex-project/projects)

---

**Built with ❤️ for local-first AI education**
