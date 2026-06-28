@echo off
setlocal

cd /d "C:\Users\Yochi\Desktop\tender-watcher"

if not exist logs mkdir logs

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy"') do set "YEAR=%%i"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format MM"') do set "MONTH=%%i"
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'"') do set "NOW=%%i"
for /f "delims=" %%i in ('git rev-parse --short HEAD') do set "GIT_COMMIT=%%i"

call ".venv\Scripts\activate.bat"

for /f "delims=" %%i in ('python -c "import sys; print(sys.version.split()[0])"') do set "PYTHON_VERSION=%%i"

if not exist "logs\%YEAR%" mkdir "logs\%YEAR%"

set "LOGFILE=logs\%YEAR%\%MONTH%.log"

echo.>>"%LOGFILE%"
echo =============================================================>>"%LOGFILE%"
echo Run started : %NOW%>>"%LOGFILE%"
echo Git Commit  : %GIT_COMMIT%>>"%LOGFILE%"
echo Python      : %PYTHON_VERSION%>>"%LOGFILE%"
echo =============================================================>>"%LOGFILE%"

python -X utf8 -m src.main >>"%LOGFILE%" 2>&1

echo =============================================================>>"%LOGFILE%"
echo Run finished: %date% %time%>>"%LOGFILE%"
echo =============================================================>>"%LOGFILE%"

endlocal