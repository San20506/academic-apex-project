@echo off
REM Academic Apex Theme Overlay Launcher
REM Standalone offline theme controller

title Academic Apex - Theme Overlay

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 Academic Apex Theme Overlay                 ║
echo ║                    Standalone Launcher                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Change to project directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

REM Check if theme overlay exists
if not exist "theme_overlay.py" (
    echo ❌ Error: theme_overlay.py not found
    echo Please ensure the theme overlay file is present.
    pause
    exit /b 1
)

echo ✅ Python detected
echo 🚀 Starting Academic Apex Theme Overlay...
echo.
echo Features:
echo • Standalone offline operation
echo • 5 predefined themes + custom colors
echo • Windows CMD theme integration
echo • Draggable overlay window
echo • Always-on-top capability
echo.

python theme_overlay.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Theme overlay exited with error
    pause
) else (
    echo.
    echo ✅ Theme overlay closed normally
)

exit /b 0
