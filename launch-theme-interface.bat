@echo off
REM Academic Apex Slider Theme Interface Launcher
REM This batch file starts the theme interface and applies CMD theming

title Academic Apex - Theme Interface Launcher

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    Academic Apex Theme                      ║
echo ║                     Interface Launcher                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Change to project directory
cd /d "%~dp0"
echo Current directory: %CD%

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

REM Check if required Python files exist
if not exist "agentforge_academic_apex\slider_theme_controller.py" (
    echo ❌ Error: slider_theme_controller.py not found
    echo Please ensure all project files are present.
    pause
    exit /b 1
)

echo ✅ Python detected: 
python --version

echo.
echo Starting Academic Apex Theme Interface...
echo.
echo Available options:
echo 1. Launch theme interface (default)
echo 2. Apply CMD theme only
echo 3. Launch interface without auto-opening browser
echo 4. View help
echo.

set /p choice="Enter your choice (1-4, or press Enter for default): "

if "%choice%"=="" set choice=1
if "%choice%"=="1" goto :launch_interface
if "%choice%"=="2" goto :apply_cmd_only
if "%choice%"=="3" goto :launch_no_browser
if "%choice%"=="4" goto :show_help

echo Invalid choice. Using default option...

:launch_interface
echo.
echo 🚀 Launching Academic Apex Theme Interface...
echo    - Interface will open at http://localhost:5002
echo    - Browser will open automatically
echo    - Press Ctrl+C to stop the server
echo.

cd agentforge_academic_apex
python slider_theme_controller.py
goto :end

:apply_cmd_only
echo.
echo 🎨 Applying CMD theme only...
echo.

cd agentforge_academic_apex
python slider_theme_controller.py --apply-cmd

if %errorlevel% equ 0 (
    echo.
    echo ✅ CMD theme applied successfully!
    echo Open a new Command Prompt window to see the changes.
) else (
    echo.
    echo ❌ Failed to apply CMD theme.
    echo Check the error messages above for details.
)
pause
goto :end

:launch_no_browser
echo.
echo 🚀 Launching Academic Apex Theme Interface (no auto-browser)...
echo    - Interface will be available at http://localhost:5002
echo    - Manually open your browser and navigate to the URL above
echo    - Press Ctrl+C to stop the server
echo.

cd agentforge_academic_apex
python slider_theme_controller.py --no-open
goto :end

:show_help
echo.
echo Academic Apex Slider Theme Interface Help
echo ========================================
echo.
echo This launcher provides an easy way to start the Academic Apex
echo theme interface and apply theming to Windows Command Prompt.
echo.
echo Features:
echo • Interactive slider controls for AI model parameters
echo • Real-time system status monitoring  
echo • Windows CMD theme application
echo • Configuration export/import
echo • Integration with Academic Apex curator service
echo.
echo Manual Usage:
echo   python agentforge_academic_apex\slider_theme_controller.py [options]
echo.
echo Options:
echo   --port PORT          Port for theme interface (default: 5002)
echo   --no-open           Don't auto-open browser
echo   --apply-cmd         Apply CMD theme and exit
echo   --config PATH       Path to theme configuration file
echo.
echo For CMD theme only:
echo   powershell -ExecutionPolicy Bypass -File apply-cmd-theme.ps1
echo.
pause
goto :end

:end
echo.
echo Thank you for using Academic Apex Theme Interface!
echo.
pause
