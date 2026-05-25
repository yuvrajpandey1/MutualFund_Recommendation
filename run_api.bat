@echo off
REM Start FastAPI Backend
REM This script activates the virtual environment and runs the FastAPI server

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting FastAPI Backend...
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

pause
