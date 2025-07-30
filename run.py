#!/usr/bin/env python3
"""
Simple startup script for GenHealth API
Run with: python run.py
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting GenHealth API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 