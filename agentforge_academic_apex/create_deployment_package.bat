@echo off
echo ==========================================
echo   Creating Deployment Package
echo ==========================================
echo.

REM Check if executable exists
if not exist "dist\AcademicApexStrategist.exe" (
    echo ERROR: Executable not found!
    echo Please run build_exe.bat first
    pause
    exit /b 1
)

echo Creating deployment package...
echo.

REM Create deployment directory
set DEPLOY_DIR=AcademicApexStrategist_v1.0
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"

echo ✓ Created deployment directory

REM Copy executable
copy "dist\AcademicApexStrategist.exe" "%DEPLOY_DIR%\"
echo ✓ Copied executable

REM Copy documentation
copy "README_EXECUTABLE.md" "%DEPLOY_DIR%\README.md"
copy "QUICK_START.md" "%DEPLOY_DIR%\"
echo ✓ Copied documentation

REM Create quick start script for the executable
echo @echo off > "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo ========================================== >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo   Academic Apex Strategist v1.0 >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo ========================================== >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo. >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo Starting Academic Apex Strategist... >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo Web Interface: http://localhost:5000 >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo. >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo Press Ctrl+C to stop >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo ========================================== >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo echo. >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo AcademicApexStrategist.exe >> "%DEPLOY_DIR%\Run_AcademicApex.bat"
echo pause >> "%DEPLOY_DIR%\Run_AcademicApex.bat"

echo ✓ Created launcher script

REM Create environment setup script
echo @echo off > "%DEPLOY_DIR%\setup_environment.bat"
echo echo ========================================== >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo   Academic Apex Environment Setup >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo ========================================== >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo. >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo This script helps you set up environment variables >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo for Academic Apex Strategist. >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo. >> "%DEPLOY_DIR%\setup_environment.bat"
echo set /p vault_path="Enter Obsidian vault path (optional): " >> "%DEPLOY_DIR%\setup_environment.bat"
echo if not "%%vault_path%%"=="" ( >> "%DEPLOY_DIR%\setup_environment.bat"
echo     setx OBSIDIAN_VAULT_PATH "%%vault_path%%" >> "%DEPLOY_DIR%\setup_environment.bat"
echo     echo ✓ Set OBSIDIAN_VAULT_PATH=%%vault_path%% >> "%DEPLOY_DIR%\setup_environment.bat"
echo ^) >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo. >> "%DEPLOY_DIR%\setup_environment.bat"
echo set /p port="Enter web UI port (default 5000): " >> "%DEPLOY_DIR%\setup_environment.bat"
echo if not "%%port%%"=="" ( >> "%DEPLOY_DIR%\setup_environment.bat"
echo     setx WEB_UI_PORT "%%port%%" >> "%DEPLOY_DIR%\setup_environment.bat"
echo     echo ✓ Set WEB_UI_PORT=%%port%% >> "%DEPLOY_DIR%\setup_environment.bat"
echo ^) >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo. >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo Environment setup complete! >> "%DEPLOY_DIR%\setup_environment.bat"
echo echo You may need to restart your command prompt >> "%DEPLOY_DIR%\setup_environment.bat"
echo pause >> "%DEPLOY_DIR%\setup_environment.bat"

echo ✓ Created environment setup script

REM Create installation checklist
echo # 📋 Installation Checklist > "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo ## ✅ Prerequisites >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - [ ] Windows 10/11 (64-bit) >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - [ ] **Ollama installed** from [ollama.ai](https://ollama.ai/download) >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - [ ] **AI models installed**: >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo   - [ ] `ollama pull mistral-7b` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo   - [ ] `ollama pull deepseek-coder` (optional) >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo ## 🚀 Quick Start >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo 1. **Extract** this folder anywhere on your computer >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo 2. **Run** `setup_environment.bat` (optional - for Obsidian integration) >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo 3. **Start Ollama**: Open cmd and run `ollama serve` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo 4. **Run Academic Apex**: Double-click `Run_AcademicApex.bat` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo 5. **Open browser** to: http://localhost:5000 >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo ## 🔧 Troubleshooting >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo **Executable won't start?** >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - Run from command line: `AcademicApexStrategist.exe` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - Check if Ollama is running: `ollama list` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo **Port conflicts?** >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - Set different port: `set WEB_UI_PORT=5001` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo. >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo **Need help?** >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - Read the full `README.md` >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"
echo - Check system status on the dashboard >> "%DEPLOY_DIR%\INSTALLATION_CHECKLIST.md"

echo ✓ Created installation checklist

REM Create version info
echo Academic Apex Strategist v1.0 > "%DEPLOY_DIR%\VERSION.txt"
echo Build Date: %DATE% %TIME% >> "%DEPLOY_DIR%\VERSION.txt"
echo. >> "%DEPLOY_DIR%\VERSION.txt"
echo Self-contained Windows executable >> "%DEPLOY_DIR%\VERSION.txt"
echo No Python installation required >> "%DEPLOY_DIR%\VERSION.txt"
echo. >> "%DEPLOY_DIR%\VERSION.txt"
echo File size: >> "%DEPLOY_DIR%\VERSION.txt"
for %%I in (dist\AcademicApexStrategist.exe) do echo   Executable: %%~zI bytes >> "%DEPLOY_DIR%\VERSION.txt"

echo ✓ Created version info

REM Calculate total package size
echo.
echo Package contents:
dir "%DEPLOY_DIR%" /s

echo.
echo ==========================================
echo   Deployment Package Complete!
echo ==========================================
echo.
echo 📁 Package location: %DEPLOY_DIR%\
echo 📦 Ready for distribution!
echo.
echo Package includes:
echo   ✓ AcademicApexStrategist.exe (standalone executable)
echo   ✓ README.md (complete documentation)
echo   ✓ QUICK_START.md (getting started guide)
echo   ✓ Run_AcademicApex.bat (easy launcher)
echo   ✓ setup_environment.bat (environment setup)
echo   ✓ INSTALLATION_CHECKLIST.md (step-by-step guide)
echo   ✓ VERSION.txt (version information)
echo.
echo The entire package can be:
echo   • Copied to any Windows computer
echo   • Distributed via USB/network/cloud
echo   • Installed without admin privileges
echo   • Run without Python installation
echo.

set /p create_zip="Create ZIP archive for distribution? (y/n): "
if /i "%create_zip%"=="y" (
    echo.
    echo Creating ZIP archive...
    powershell -command "Compress-Archive -Path '%DEPLOY_DIR%' -DestinationPath '%DEPLOY_DIR%.zip' -Force"
    if exist "%DEPLOY_DIR%.zip" (
        echo ✅ ZIP created: %DEPLOY_DIR%.zip
        for %%I in ("%DEPLOY_DIR%.zip") do echo    Size: %%~zI bytes
    ) else (
        echo ❌ Failed to create ZIP archive
    )
)

echo.
echo 🎉 Deployment package is ready!
pause
