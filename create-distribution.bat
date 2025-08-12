@echo off
REM Create distribution package for Academic Apex Theme Overlay

title Creating Distribution Package

echo.
echo 📦 Creating Academic Apex Theme Overlay Distribution Package...
echo.

REM Create distribution folder name with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set today=%%c%%a%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set now=%%a%%b
set timestamp=%today%-%now%
set distname=AcademicApexThemeOverlay-%timestamp%

echo 📁 Creating package: %distname%
mkdir "%distname%" 2>nul

REM Copy files to distribution package
echo 📋 Copying distribution files...
copy "dist\AcademicApexThemeOverlay.exe" "%distname%\" >nul
copy "dist\apply-cmd-theme.ps1" "%distname%\" >nul
copy "dist\README-Overlay.md" "%distname%\" >nul
copy "dist\DISTRIBUTION-README.md" "%distname%\README.md" >nul

REM Create a simple launcher
echo @echo off > "%distname%\Launch.bat"
echo echo 🎨 Starting Academic Apex Theme Overlay... >> "%distname%\Launch.bat"
echo start "" "AcademicApexThemeOverlay.exe" >> "%distname%\Launch.bat"
echo exit >> "%distname%\Launch.bat"

echo ✅ Package created successfully!
echo.
echo 📊 Package Contents:
echo   📂 %distname%\
echo   ├── 📄 AcademicApexThemeOverlay.exe (11MB - Standalone)
echo   ├── 📄 apply-cmd-theme.ps1 (PowerShell script)
echo   ├── 📄 Launch.bat (Quick launcher)
echo   ├── 📄 README.md (User instructions)
echo   └── 📄 README-Overlay.md (Full documentation)
echo.
echo 🎯 Ready for Distribution:
echo   • Copy the '%distname%' folder to any Windows computer
echo   • No Python installation required
echo   • Double-click Launch.bat or AcademicApexThemeOverlay.exe to start
echo   • Works on Windows 7/8/10/11
echo.

pause
