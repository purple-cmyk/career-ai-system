#!/bin/bash

echo "=================================="
echo "Career AI - Setup Script"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python 3 found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+"
    exit 1
fi

echo "✅ Node.js found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup frontend
echo ""
echo "📦 Installing React dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To run the application:"
echo ""
echo "1. Start Backend (in one terminal):"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "2. Start Frontend (in another terminal):"
echo "   cd frontend && npm start"
echo ""
echo "Then open: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
