@echo off
setlocal
cd /d "%~dp0"

if exist build_fixed rmdir /s /q build_fixed
if exist dist_fixed rmdir /s /q dist_fixed

..\venv\Scripts\python.exe -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --windowed ^
  --name WinLoadASCEApp_fixed ^
  --distpath dist_fixed ^
  --workpath build_fixed ^
  --specpath . ^
  --add-data "app\web\templates;app\web\templates" ^
  --add-data "app\web\static;app\web\static" ^
  --add-data "sample_data;sample_data" ^
  desktop_launcher.py

echo.
echo Build complete. EXE is in dist_fixed\WinLoadASCEApp_fixed\
pause
