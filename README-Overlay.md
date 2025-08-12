# Academic Apex Theme Overlay

A **standalone offline desktop overlay** application for managing themes. No web browser required - works completely offline as a desktop application.

## 🎯 Key Features

### 🎨 **Pure Theme Focus**
- **5 Predefined Themes**: Academic Apex, Dark Professional, Blue Steel, Green Matrix, Purple Haze
- **Custom Colors**: Click any color button to choose your own colors
- **Real-time Preview**: See changes instantly
- **Windows CMD Integration**: Apply themes to Command Prompt

### 🖥️ **Desktop Overlay**
- **Always-on-Top**: Stays visible over other applications
- **Draggable**: Move anywhere on screen by dragging the header
- **Minimizable**: Collapse to header-only view with the "−" button
- **Transparent**: Semi-transparent for minimal desktop clutter

### 📴 **Completely Offline**
- **No Web Browser**: Pure desktop application using tkinter
- **No Internet Required**: All functionality works offline
- **No AI Models**: Focused solely on theme management
- **Lightweight**: Single Python file with minimal dependencies

## 🚀 Quick Start

### Method 1: Easy Launch
1. **Double-click** `launch-theme-overlay.bat`
2. The overlay window appears on your desktop
3. Start customizing themes immediately!

### Method 2: Direct Python
```bash
python theme_overlay.py
```

## 🎛️ How to Use

### Theme Selection
- **Choose from 5 predefined themes** using radio buttons
- **Academic Apex**: Professional blue theme (default)
- **Dark Professional**: GitHub-style dark theme  
- **Blue Steel**: Discord-inspired theme
- **Green Matrix**: Retro green terminal theme
- **Purple Haze**: Purple gradient theme
- **Custom**: Use your own color selections

### Color Customization
- **Click any color button** to open the color picker
- **Live updates** - see changes immediately
- **5 main colors**: Background, Accent, Success, Warning, Error
- **Color codes displayed** on each button

### Actions
- **Apply CMD Theme**: Applies your theme to Windows Command Prompt
- **Preview Theme**: Opens a separate preview window
- **Reset to Default**: Restores Academic Apex theme
- **Save Configuration**: Saves your settings to file

### Overlay Controls
- **Drag the header** to move the window anywhere
- **Minimize button (−)**: Collapse to header-only view
- **Double-click title**: Toggle always-on-top behavior
- **Close window**: Saves settings and exits

## 🎨 Available Themes

| Theme | Description | Colors |
|-------|-------------|--------|
| **Academic Apex** | Professional blue theme | Dark gray + bright blue accents |
| **Dark Professional** | GitHub-style dark | Very dark + subtle blue highlights |
| **Blue Steel** | Discord-inspired | Dark blue-gray + purple accents |
| **Green Matrix** | Retro terminal style | Dark blue + bright green highlights |
| **Purple Haze** | Purple gradient theme | Dark purple + bright purple accents |
| **Custom** | Your own colors | Whatever you choose! |

## 💾 Configuration

Settings are automatically saved to `theme_overlay_config.json`:

```json
{
  "theme_name": "Academic Apex Theme",
  "version": "1.0.0",
  "colors": {
    "primary_bg": "#1a1a1a",
    "secondary_bg": "#2d2d2d", 
    "accent_color": "#4a9eff",
    "success_color": "#4caf50",
    "warning_color": "#ff9800",
    "error_color": "#f44336"
  },
  "overlay_settings": {
    "always_on_top": true,
    "transparency": 0.95,
    "position_x": 100,
    "position_y": 100
  }
}
```

## 🖼️ Windows CMD Integration

The overlay can apply your chosen theme to Windows Command Prompt:

1. **Choose your theme** in the overlay
2. **Click "Apply CMD Theme"** 
3. **Open a new Command Prompt** to see the changes

### What Gets Applied
- **Color scheme** matching your overlay theme
- **Enhanced font** (Consolas 12pt)
- **Improved settings** (QuickEdit, better history)
- **Automatic backup** of original settings

## 🛠️ Technical Details

### Requirements
- **Python 3.7+** with tkinter (usually included)
- **Windows OS** (for CMD theme integration)
- **PowerShell** (for CMD theme script)

### Dependencies
- **tkinter**: Built-in Python GUI library
- **json**: Configuration file handling
- **subprocess**: For running PowerShell scripts
- **pathlib**: File system operations

### File Structure
```
academic-apex-project/
├── theme_overlay.py              # Main overlay application
├── launch-theme-overlay.bat      # Easy launcher
├── apply-cmd-theme.ps1          # PowerShell CMD theme script
├── theme_overlay_config.json    # Settings (auto-generated)
└── README-Overlay.md            # This documentation
```

## 🔧 Customization

### Adding New Themes
Edit the `themes` dictionary in `theme_overlay.py`:

```python
"my_custom_theme": {
    "primary_bg": "#your_bg_color",
    "secondary_bg": "#your_secondary_color",
    "accent_color": "#your_accent_color",
    "success_color": "#your_success_color", 
    "warning_color": "#your_warning_color",
    "error_color": "#your_error_color"
}
```

### Modifying Overlay Behavior
- **Window size**: Change `self.root.geometry("350x500+100+100")`
- **Transparency**: Modify `self.root.wm_attributes("-alpha", 0.95)`
- **Always on top**: Toggle `self.root.wm_attributes("-topmost", True)`

## 🐛 Troubleshooting

### Common Issues

**Overlay won't start:**
- Check Python is installed: `python --version`
- Ensure tkinter is available: `python -c "import tkinter"`

**CMD theme not applying:**
- Run as Administrator (recommended)  
- Check if PowerShell script exists: `apply-cmd-theme.ps1`
- Verify PowerShell execution policy allows scripts

**Colors not saving:**
- Check write permissions in project folder
- Ensure `theme_overlay_config.json` isn't read-only

**Window not draggable:**
- Make sure to drag the **header area** (dark gray bar)
- Don't try to drag other parts of the window

### Reset Everything
Delete `theme_overlay_config.json` and restart the overlay to reset all settings to defaults.

## ⚡ Performance

- **Minimal Resource Usage**: Pure tkinter application
- **No Background Services**: Only runs when window is open
- **Fast Startup**: Loads in under 1 second
- **Small Footprint**: ~50KB Python file

## 📄 License

MIT License - Same as the Academic Apex project

---

## 🎯 Perfect For

- **Theme Enthusiasts**: Quick theme switching without browser overhead
- **Developers**: Color coding for different projects
- **Productivity Users**: Always-on-top overlay for theme management  
- **Offline Work**: No internet dependency
- **Windows Users**: Integrated CMD theming

**Academic Apex Theme Overlay** - Simple, Fast, Offline Theme Management
