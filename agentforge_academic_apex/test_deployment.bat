@echo off
echo ==========================================
echo   Testing Academic Apex Deployment
echo ==========================================
echo.

echo Testing deployment package...
cd AcademicApexStrategist_v1.0

echo.
echo Checking files:
if exist "AcademicApexStrategist.exe" (
    echo ✓ AcademicApexStrategist.exe found
) else (
    echo ❌ AcademicApexStrategist.exe missing
)

if exist "Run_AcademicApex.bat" (
    echo ✓ Run_AcademicApex.bat found
) else (
    echo ❌ Run_AcademicApex.bat missing
)

if exist "README.md" (
    echo ✓ README.md found
) else (
    echo ❌ README.md missing
)

echo.
echo Testing executable startup (5 seconds)...
timeout /t 1 >nul
start /min cmd /c "AcademicApexStrategist.exe > test_output.txt 2>&1 & timeout /t 5 & taskkill /f /im AcademicApexStrategist.exe >nul 2>&1"

echo Waiting for test to complete...
timeout /t 8 >nul

if exist "test_output.txt" (
    echo ✓ Executable ran successfully
    echo.
    echo First few lines of output:
    type test_output.txt | head -10
    del test_output.txt
) else (
    echo ❌ Executable test failed
)

echo.
echo ==========================================
echo   Deployment test complete!
echo ==========================================

cd ..
pause
