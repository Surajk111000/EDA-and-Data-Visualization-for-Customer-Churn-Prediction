#!/bin/bash
# Quick start script for EDA Dashboard (macOS/Linux)
# This script sets up and runs the Streamlit app

echo ""
echo "========================================"
echo "  EDA Dashboard - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[OK] Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "[OK] Virtual environment activated"
echo ""

# Check if requirements are installed
if ! pip show streamlit &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install requirements"
        exit 1
    fi
    echo "[OK] Dependencies installed"
else
    echo "[OK] Dependencies already installed"
fi

echo ""
echo "========================================"
echo "  Starting Streamlit Application"
echo "========================================"
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
streamlit run app.py
