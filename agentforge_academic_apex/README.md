# Academic Apex Strategist

A comprehensive AI-powered academic assistant that creates study plans, diagnostic quizzes, and learning materials using local Ollama models and Obsidian vault integration.

## 🎯 Features

- **Diagnostic Quiz Generation**: Create comprehensive quizzes to assess student knowledge
- **Study Plan Creation**: Generate detailed minute-by-minute study plans with active learning techniques
- **Code Module Generation**: Build Python utilities for academic tasks
- **Obsidian Integration**: Seamlessly save notes and plans to your Obsidian vault
- **Prompt Curation**: Advanced prompt refinement using local models for better results
- **Local-First**: Runs entirely on your machine using Ollama - no external API calls

## 🏗️ Architecture

```
Academic Apex Strategist
├── ollama_adapter.py      # Ollama API client with robust error handling
├── curator_service.py     # Flask service for prompt refinement
├── obsidian_adapter.py    # Obsidian vault integration
├── smoke_tests.py         # Comprehensive testing suite
├── agent.yml              # AgentForge manifest
├── requirements.txt       # Python dependencies
└── generated/             # Output directory for generated content
```

## 📋 Prerequisites

### Required Software
- **Python 3.10+**: For running the Python components
- **Ollama**: Local LLM service ([Installation Guide](https://ollama.ai/download))
- **Git**: For version control (optional)

### Required Ollama Models
```bash
ollama pull deepseek-coder    # Primary model for content generation
ollama pull mistral-7b        # Curator model for prompt refinement
```

### Optional but Recommended
- **Obsidian**: For note management ([Download](https://obsidian.md))

## ⚡ Quick Start

### 1. Environment Setup

```bash
# Clone or navigate to project directory
cd academic-apex-project/agentforge_academic_apex

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Ollama Service

```bash
# Ensure Ollama is running
ollama serve

# In another terminal, verify models are available
ollama list
# Should show deepseek-coder and mistral-7b
```

### 3. Configure Environment Variables

```bash
# Required for Obsidian integration (replace with your vault path)
export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"

# Optional configurations (defaults shown)
export OLLAMA_HOST="http://localhost:11434"
export CURATOR_MODEL="mistral-7b"
export CURATOR_SERVICE_URL="http://localhost:5001"
```

**Windows PowerShell:**
```powershell
$env:OBSIDIAN_VAULT_PATH="C:\path\to\your\obsidian\vault"
$env:OLLAMA_HOST="http://localhost:11434"
$env:CURATOR_MODEL="mistral-7b"
```

### 4. Start the Curator Service

```bash
# Start the prompt curation service
python curator_service.py
```

The service will start on `http://localhost:5001` and provide:
- Health check: `GET /healthz`
- Prompt curation: `POST /api/curate`

### 5. Run Smoke Tests

```bash
# Run comprehensive tests to verify everything works
python smoke_tests.py
```

This will test all components and generate sample outputs in the `generated/` directory.

## 🚀 Usage Examples

### Basic Component Testing

```python
from ollama_adapter import OllamaAdapter
from obsidian_adapter import ObsidianAdapter

# Test Ollama connection
adapter = OllamaAdapter()
if adapter.test_connection():
    print("Ollama is ready!")
    
    # Generate content
    result = adapter.generate("Explain quantum computing in simple terms")
    print(result["text"])

# Test Obsidian integration
vault_path = "/path/to/your/vault"
obs = ObsidianAdapter(vault_path)
obs.create_note("Test Note", "This is a test note from Academic Apex")
```

### Curator Service Usage

```python
import requests

# Refine a prompt
response = requests.post("http://localhost:5001/api/curate", json={
    "prompt": "Create a quiz about Python",
    "instruction": "Make it more detailed and educational"
})

refined_prompt = response.json()["refined"]
print(refined_prompt)
```

## 📁 Generated Content Structure

The system creates organized content in your Obsidian vault:

```
YourObsidianVault/
└── AcademicApex/
    ├── StudyPlans/
    │   └── StudyPlan_MachineLearning_20250112_143022.md
    ├── Quizzes/
    │   └── Quiz_PythonBasics_20250112_143045.md
    └── CodeModules/
        └── Note_GeneratedCode_20250112_143108.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OBSIDIAN_VAULT_PATH` | ✅ | - | Path to your Obsidian vault directory |
| `OLLAMA_HOST` | ❌ | `http://localhost:11434` | Ollama API endpoint |
| `CURATOR_MODEL` | ❌ | `mistral-7b` | Model for prompt curation |
| `CURATOR_SERVICE_URL` | ❌ | `http://localhost:5001` | Curator service URL |

### Model Configuration

You can customize the models used by editing the adapters:

```python
# Use different primary model
adapter = OllamaAdapter(model="codellama")

# Or specify per request
result = adapter.generate(prompt, model="mistral-7b")
```

## 🧪 Testing

The project includes comprehensive smoke tests:

```bash
# Run all tests
python smoke_tests.py

# Run individual component tests
python ollama_adapter.py      # Test Ollama integration
python obsidian_adapter.py    # Test Obsidian integration
```

### Test Coverage

- ✅ Ollama connectivity and model availability
- ✅ Prompt curation service functionality
- ✅ Obsidian vault creation and note management
- ✅ Diagnostic quiz generation with validation
- ✅ Study plan creation with timeline structure
- ✅ Python code generation with syntax validation

## 🔍 Troubleshooting

### Common Issues

**🚨 "Ollama connection failed"**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

**🚨 "Curator service unreachable"**
```bash
# Start the curator service
python curator_service.py

# Check health
curl http://localhost:5001/healthz
```

**🚨 "Vault validation failed"**
```bash
# Check if path exists and is writable
ls -la "$OBSIDIAN_VAULT_PATH"

# Create directory if needed
mkdir -p "$OBSIDIAN_VAULT_PATH"
```

**🚨 "Model not found"**
```bash
# Pull required models
ollama pull deepseek-coder
ollama pull mistral-7b

# List available models
ollama list
```

### Performance Optimization

**For Low-Resource Systems:**
- Use smaller models: `mistral-7b` instead of `deepseek-coder`
- Reduce `max_tokens` in generation calls
- Lower `temperature` for more deterministic outputs

**For Better Performance:**
- Ensure sufficient RAM (8GB+ recommended)
- Use SSD storage for faster model loading
- Consider GPU acceleration if available

### Logging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or check logs in the `logs/` directory (created automatically).

## 🔄 Integration with AgentForge

This agent is designed to work with AgentForge. The `agent.yml` manifest defines:

- Task schemas for quiz generation, study planning, and code creation
- Integration points with Ollama and Obsidian
- Environment requirements and health checks
- Fallback behaviors for offline operation

## 📦 Deployment

### Local Development
```bash
# Start all services
ollama serve &
python curator_service.py &

# Run tests to verify
python smoke_tests.py
```

### Docker Support (Optional)

```bash
# Build and run with Docker
docker-compose up -d
```

This starts both Ollama and the curator service in containers.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run smoke tests: `python smoke_tests.py`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Roadmap

- [ ] Web interface for non-technical users
- [ ] Support for additional LLM providers
- [ ] Enhanced quiz formats (visual, interactive)
- [ ] Study plan templates and presets
- [ ] Progress tracking and analytics
- [ ] Multi-language support

## 💡 Tips for Best Results

### Prompt Engineering
- Be specific about requirements and format
- Use the curator service for complex prompts
- Provide examples when possible

### Study Plan Generation
- Specify exact duration and learning objectives
- Include difficulty level and prior knowledge
- Mention preferred learning styles

### Quiz Creation
- Define the target audience and difficulty
- Specify question types and topics to cover
- Include number of questions needed

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Run `python smoke_tests.py` to diagnose problems
3. Check Ollama service status and logs
4. Ensure all environment variables are set correctly

---

**Built with ❤️ for educators and students who value privacy and local-first AI solutions.**
