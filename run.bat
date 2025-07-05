@echo off
REM run.bat for Windows

:: 1. Create virtual environment
python -m venv venv

:: 2. Activate virtual environment
call venv\Scripts\activate.bat

:: 3. Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

:: 4. Run FastAPI app
uvicorn app:app --reload
