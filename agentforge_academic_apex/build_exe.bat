@echo off
echo ==========================================
echo   Building Academic Apex Strategist EXE
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

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Checking project files...

REM Verify required files exist
if not exist "main_launcher.py" (
    echo ERROR: main_launcher.py not found
    pause
    exit /b 1
)

if not exist "web_ui.py" (
    echo ERROR: web_ui.py not found
    pause
    exit /b 1
)

if not exist "curator_service.py" (
    echo ERROR: curator_service.py not found
    pause
    exit /b 1
)

if not exist "ollama_adapter.py" (
    echo ERROR: ollama_adapter.py not found
    pause
    exit /b 1
)

if not exist "templates\" (
    echo ERROR: templates directory not found
    pause
    exit /b 1
)

echo ✓ All required files found

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Cleaning previous builds...
if exist "dist\" rmdir /s /q "dist"
if exist "build\" rmdir /s /q "build"
if exist "*.spec~" del "*.spec~"

echo.
echo ==========================================
echo   Building executable...
echo ==========================================
echo.
echo This may take several minutes...

REM Use the custom spec file
python -m PyInstaller academic_apex.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ BUILD FAILED!
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Build Complete!
echo ==========================================

if exist "dist\AcademicApexStrategist.exe" (
    echo.
    echo ✅ SUCCESS: Executable created!
    echo 📁 Location: dist\AcademicApexStrategist.exe
    echo 📏 File size: 
    for %%I in (dist\AcademicApexStrategist.exe) do echo    %%~zI bytes
    echo.
    echo ==========================================
    echo   Next Steps:
    echo ==========================================
    echo 1. Test the executable: .\dist\AcademicApexStrategist.exe
    echo 2. Make sure Ollama is running: ollama serve
    echo 3. Ensure models are installed: ollama pull mistral-7b
    echo 4. Set environment variables if needed
    echo.
    echo The executable is completely self-contained!
    echo No Python installation required on target systems.
    echo.
    set /p test="Would you like to test the executable now? (y/n): "
    if /i "%test%"=="y" (
        echo.
        echo Starting executable...
        echo Press Ctrl+C to stop when ready
        echo.
        .\dist\AcademicApexStrategist.exe
    )
) else (
    echo.
    echo ❌ ERROR: Executable not found after build
    echo Check the PyInstaller output above for errors
)

echo.
echo Press any key to exit...
pause >nul
