@echo off
REM Quick start script for EDA Dashboard (Windows)
REM This script sets up and runs the Streamlit app

echo.
echo ========================================
echo  EDA Dashboard - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo [OK] Virtual environment activated
echo.

REM Check if requirements are installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.
echo ========================================
echo  Starting Streamlit Application
echo ========================================
echo.
echo Dashboard will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
pause

REM Run the application
streamlit run app.py

pause
