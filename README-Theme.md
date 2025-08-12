# Academic Apex Slider Theme Interface

A comprehensive theme system with interactive slider controls for the Academic Apex Strategist project, featuring both web interface theming and Windows Command Prompt integration.

## 🎨 Features

### Slider Interface
- **Interactive Controls**: Real-time slider adjustments for AI model parameters
- **Dark Theme**: Professional dark theme with accent colors
- **Responsive Design**: Works on desktop and mobile devices
- **Live Console**: Terminal-style output with colored text
- **Status Monitoring**: Real-time system and service status indicators

### Windows CMD Integration
- **Complete Theme**: Applies Academic Apex colors to Windows Command Prompt
- **Professional Appearance**: Dark background with optimized color scheme
- **Enhanced Settings**: Improved font, cursor, and window configuration
- **Registry Safe**: Creates backups before applying changes

### Model Configuration
- **Temperature Control**: Fine-tune response creativity (0.0 - 1.0)
- **Token Limits**: Adjust maximum response length (100 - 4000)
- **Top-p Sampling**: Control response diversity (0.1 - 1.0)
- **Timeout Settings**: Configure API timeouts (30 - 300 seconds)
- **Retry Logic**: Set retry attempts for failed requests (1 - 10)

## 🚀 Quick Start

### Method 1: Easy Launch (Recommended)
1. Double-click `launch-theme-interface.bat`
2. Choose option 1 for the full interface
3. Your browser will open automatically to `http://localhost:5002`

### Method 2: Command Line
```bash
# Start the full interface
python agentforge_academic_apex\slider_theme_controller.py

# Apply CMD theme only
python agentforge_academic_apex\slider_theme_controller.py --apply-cmd

# Start without auto-opening browser
python agentforge_academic_apex\slider_theme_controller.py --no-open --port 5003
```

### Method 3: PowerShell (CMD Theme Only)
```powershell
# Apply CMD theme with backup
powershell -ExecutionPolicy Bypass -File apply-cmd-theme.ps1 -Backup

# Force application (skip backup)
powershell -ExecutionPolicy Bypass -File apply-cmd-theme.ps1 -Force
```

## 📁 File Structure

```
academic-apex-project/
├── slider_theme_interface.html      # Main web interface
├── apply-cmd-theme.ps1             # PowerShell CMD theming script
├── launch-theme-interface.bat      # Windows launcher script
├── README-Theme.md                 # This documentation
├── agentforge_academic_apex/
│   ├── slider_theme_controller.py  # Python theme controller
│   ├── curator_service.py          # Existing curator service
│   └── ollama_adapter.py           # Existing Ollama adapter
└── theme_config.json               # Theme configuration (auto-generated)
```

## 🎛️ Interface Controls

### Model Configuration Panel
- **Temperature Slider**: Controls response randomness and creativity
- **Max Tokens Slider**: Sets the maximum length of generated responses
- **Top-p Slider**: Controls nucleus sampling for response diversity

### System Controls Panel  
- **API Timeout**: Maximum time to wait for API responses
- **Retry Attempts**: Number of retry attempts for failed requests
- **Action Buttons**: Test connections, apply settings, reset defaults

### Actions Panel
- **Start Curator Service**: Launches the Academic Apex curator on port 5001
- **List Available Models**: Shows all available Ollama models
- **Apply CMD Theme**: Applies the theme to Windows Command Prompt
- **Export Settings**: Downloads current configuration as JSON

### Console Output
- **Real-time Feedback**: Live output from system operations
- **Color-coded Messages**: Success (green), warnings (yellow), errors (red)
- **Command Prompt Style**: Familiar terminal interface

## 🎨 Theme Colors

The Academic Apex theme uses a carefully selected color palette:

| Purpose | Color | Hex Code |
|---------|-------|----------|
| Background | Dark | #1a1a1a |
| Secondary Background | Medium Dark | #2d2d2d |
| Primary Accent | Blue | #4a9eff |
| Success | Green | #4caf50 |
| Warning | Orange | #ff9800 |
| Error | Red | #f44336 |
| Primary Text | White | #ffffff |
| Secondary Text | Light Gray | #b0b0b0 |

## 🔧 Configuration

### Theme Configuration File
The system automatically creates `theme_config.json` with your settings:

```json
{
  "theme_name": "Academic Apex Slider Theme",
  "version": "1.0.0",
  "colors": {
    "primary_bg": "#1a1a1a",
    "accent_color": "#4a9eff",
    "success_color": "#4caf50"
  },
  "model_settings": {
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 0.9,
    "timeout": 120,
    "retry_attempts": 3
  }
}
```

### Command Line Options

```bash
python slider_theme_controller.py --help

Options:
  --port PORT         Port for theme interface (default: 5002)
  --no-open          Don't auto-open browser
  --apply-cmd        Apply CMD theme and exit
  --config PATH      Path to theme configuration file
```

### PowerShell Script Options

```powershell
.\apply-cmd-theme.ps1 -Backup    # Create backup before applying
.\apply-cmd-theme.ps1 -Force     # Skip confirmation prompts
```

## 🔌 Integration

### With Existing Services
The theme interface integrates seamlessly with your existing Academic Apex services:

- **Curator Service**: Monitors connection status and available models
- **Ollama Adapter**: Uses existing connection testing and model listing
- **Flask Integration**: Runs alongside the curator service on a different port

### API Endpoints
The theme controller provides REST API endpoints:

```
GET  /                     # Main interface
GET  /api/status          # System status
GET  /api/config          # Current configuration  
POST /api/config          # Update configuration
POST /api/apply-cmd-theme # Apply CMD theme
GET  /api/export-config   # Export configuration
```

## 🛠️ Customization

### Modifying Colors
Edit the CSS variables in `slider_theme_interface.html`:

```css
:root {
    --primary-bg: #1a1a1a;
    --accent-color: #4a9eff;
    /* Add your custom colors */
}
```

### Adding New Sliders
1. Add HTML slider element in the interface
2. Update JavaScript slider array
3. Add validation in `slider_theme_controller.py`

### Custom CMD Colors
Modify the `$ThemeColors` hashtable in `apply-cmd-theme.ps1`:

```powershell
$ThemeColors = @{
    'ColorTable00' = 0x1a1a1a  # Background
    'ColorTable01' = 0x4a9eff  # Your custom accent
    # Add more custom colors...
}
```

## 🔒 Security & Permissions

### Windows CMD Theming
- Modifies user-specific registry settings (HKCU:\Console)
- No administrator rights required for user settings
- Creates automatic backups before applying changes
- Can be easily reverted using backup files

### Web Interface
- Runs on localhost only by default
- No external network access required
- Configuration files stored locally
- No sensitive data transmission

## 📊 Monitoring & Logging

### System Status
The interface provides real-time monitoring of:
- Ollama service connectivity
- Available AI models
- Theme application status
- System resource information

### Logging
All operations are logged with appropriate levels:
- INFO: Normal operations and status updates
- WARNING: Non-critical issues that should be noted
- ERROR: Failed operations that require attention

## 🔄 Backup & Recovery

### CMD Theme Backups
Automatic backups are created before applying CMD themes:
- Stored as JSON files with timestamp
- Include all original registry settings
- Can be used for manual restoration

### Configuration Backups
- Export current settings anytime via the interface
- JSON format for easy editing and sharing
- Includes timestamps and system information

## 🐛 Troubleshooting

### Common Issues

**Interface won't start:**
- Check Python is installed and accessible
- Ensure all required files are present
- Try a different port with `--port` option

**CMD theme not applying:**
- Run PowerShell as Administrator (recommended)
- Check Windows version compatibility
- Verify registry access permissions

**Slider values not saving:**
- Check write permissions in project directory
- Ensure theme_config.json is not read-only
- Look for error messages in the console

**Browser doesn't auto-open:**
- Use `--no-open` and manually navigate to the URL
- Check default browser settings
- Try a different browser

### Debug Mode
Enable detailed logging by modifying the logging level in `slider_theme_controller.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

This theme system is part of the Academic Apex Strategist project. To contribute:

1. Follow the existing code style and structure
2. Test changes on Windows Command Prompt
3. Ensure mobile responsiveness for web components
4. Update documentation for new features

## 📄 License

MIT License - see the existing project license for details.

---

**Academic Apex Strategist** - Advanced AI-Powered Research & Development Interface
