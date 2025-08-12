@echo off
REM Quick build script for Academic Apex Theme Overlay EXE

echo 🚀 Quick Building Academic Apex Theme Overlay...

REM Install PyInstaller quickly
python -m pip install pyinstaller --quiet

REM Clean and build
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Build with basic options
python -m PyInstaller theme_overlay.py --onefile --windowed --name "AcademicApexThemeOverlay" --add-data "apply-cmd-theme.ps1;." --clean --noconfirm

if %errorlevel% equ 0 (
    echo ✅ Build successful! 
    echo 📂 Location: dist\AcademicApexThemeOverlay.exe
    copy "apply-cmd-theme.ps1" "dist\" >nul 2>&1
    echo 🎉 Ready to use!
) else (
    echo ❌ Build failed!
)

pause
