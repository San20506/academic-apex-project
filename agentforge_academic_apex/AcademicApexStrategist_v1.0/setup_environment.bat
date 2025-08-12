@echo off 
echo ========================================== 
echo   Academic Apex Environment Setup 
echo ========================================== 
echo. 
echo This script helps you set up environment variables 
echo for Academic Apex Strategist. 
echo. 
set /p vault_path="Enter Obsidian vault path (optional): " 
if not "%vault_path%"=="" ( 
    setx OBSIDIAN_VAULT_PATH "%vault_path%" 
    echo ✓ Set OBSIDIAN_VAULT_PATH=%vault_path% 
) 
echo. 
set /p port="Enter web UI port (default 5000): " 
if not "%port%"=="" ( 
    setx WEB_UI_PORT "%port%" 
    echo ✓ Set WEB_UI_PORT=%port% 
) 
echo. 
echo Environment setup complete! 
echo You may need to restart your command prompt 
pause 
