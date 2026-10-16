@echo off
setlocal
if exist "%~dp0.venv\Scripts\python.exe" (
  "%~dp0.venv\Scripts\python.exe" -X utf8 "%~dp0open_template.py"
) else (
  python -X utf8 "%~dp0open_template.py"
)
if errorlevel 1 pause
