@echo off
REM Academic Apex Theme Overlay - EXE Builder
REM This script builds a standalone .exe file using PyInstaller

title Building Academic Apex Theme Overlay EXE

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 Academic Apex Theme Overlay                 ║
echo ║                    EXE Builder Script                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Change to project directory
cd /d "%~dp0"
echo Current directory: %CD%

REM Check Python installation
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

python --version
echo.

REM Check if theme_overlay.py exists
if not exist "theme_overlay.py" (
    echo ❌ Error: theme_overlay.py not found
    echo Please ensure the theme overlay file is present.
    pause
    exit /b 1
)

REM Install PyInstaller if not present
echo 📦 Installing/updating build dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "__pycache__" rmdir /s /q __pycache__
echo ✅ Cleaned build directories
echo.

REM Build the executable
echo 🔨 Building standalone executable...
echo This may take a few minutes, please wait...
echo.

python -m PyInstaller theme_overlay.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    echo Check the output above for error details.
    pause
    exit /b 1
)

REM Check if build was successful
if not exist "dist\AcademicApexThemeOverlay.exe" (
    echo ❌ Build completed but executable not found!
    echo Expected: dist\AcademicApexThemeOverlay.exe
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.

REM Display file information
echo 📊 Build Results:
echo ================
for %%f in ("dist\AcademicApexThemeOverlay.exe") do (
    echo File: %%~nxf
    echo Size: %%~zf bytes (~%%~zf MB if over 1MB)
    echo Location: %CD%\dist\%%~nxf
)
echo.

REM Copy additional files to dist folder
echo 📁 Copying additional files...
copy "apply-cmd-theme.ps1" "dist\" >nul 2>&1
copy "README-Overlay.md" "dist\" >nul 2>&1

echo ✅ Additional files copied to dist folder
echo.

REM Test the executable
echo 🧪 Testing the executable...
set /p test_choice="Do you want to test the executable now? (y/n): "

if /i "%test_choice%"=="y" (
    echo Starting AcademicApexThemeOverlay.exe...
    start "" "dist\AcademicApexThemeOverlay.exe"
    echo.
    echo If the application started successfully, the build is working!
) else (
    echo Skipping test.
)

echo.
echo 🎉 Build Process Complete!
echo.
echo Your standalone executable is ready:
echo   📂 Location: %CD%\dist\
echo   📄 File: AcademicApexThemeOverlay.exe
echo   📋 Additional files: apply-cmd-theme.ps1, README-Overlay.md
echo.
echo You can now:
echo   • Run AcademicApexThemeOverlay.exe directly
echo   • Copy the entire 'dist' folder to any Windows computer
echo   • Share the executable without Python installation requirements
echo.

pause
exit /b 0
