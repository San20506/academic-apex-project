@echo off
echo ==========================================
echo   Academic Apex Strategist Startup
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ and try again
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "web_ui.py" (
    echo ERROR: Please run this script from the agentforge_academic_apex directory
    echo Current directory: %cd%
    pause
    exit /b 1
)

echo Setting up environment...
echo.

REM Set default environment variables if not already set
if not defined OLLAMA_HOST (
    set OLLAMA_HOST=http://localhost:11434
    echo Set OLLAMA_HOST=%OLLAMA_HOST%
)

if not defined CURATOR_SERVICE_URL (
    set CURATOR_SERVICE_URL=http://localhost:5001
    echo Set CURATOR_SERVICE_URL=%CURATOR_SERVICE_URL%
)

if not defined CURATOR_MODEL (
    set CURATOR_MODEL=mistral-7b
    echo Set CURATOR_MODEL=%CURATOR_MODEL%
)

if not defined WEB_UI_PORT (
    set WEB_UI_PORT=5000
    echo Set WEB_UI_PORT=%WEB_UI_PORT%
)

REM Check for Obsidian vault path
if not defined OBSIDIAN_VAULT_PATH (
    echo.
    echo WARNING: OBSIDIAN_VAULT_PATH not set!
    echo Obsidian integration will not work.
    echo Please set: set OBSIDIAN_VAULT_PATH=C:\path\to\your\vault
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        exit /b 1
    )
) else (
    echo Set OBSIDIAN_VAULT_PATH=%OBSIDIAN_VAULT_PATH%
)

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo   Starting Services
echo ==========================================
echo.

echo Starting Curator Service in background...
start "Academic Apex - Curator Service" cmd /k "python curator_service.py"

echo Waiting 3 seconds for curator to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting Web UI...
echo.
echo ==========================================
echo   Academic Apex Strategist is starting!
echo.
echo   Web Interface: http://localhost:%WEB_UI_PORT%
echo   Curator Service: %CURATOR_SERVICE_URL%
echo   Ollama Host: %OLLAMA_HOST%
echo.
echo   Press Ctrl+C to stop
echo ==========================================
echo.

python web_ui.py

echo.
echo Web UI stopped. Press any key to exit...
pause >nul
