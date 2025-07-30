#!/usr/bin/env python3
"""
Deployment Helper for GenHealth API
This script helps you deploy your API to various platforms
"""

import os
import subprocess
import sys

def print_header():
    print("🚀 GenHealth API Deployment Helper")
    print("=" * 50)

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "requirements.txt",
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/crud.py",
        "app/database.py",
        "app/utils.py",
        "app/logger.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def show_deployment_options():
    print("\n📋 Choose your deployment platform:")
    print("1. Railway (Recommended - Free & Easy)")
    print("2. Render (Free Tier Available)")
    print("3. Heroku (Paid)")
    print("4. DigitalOcean (Paid)")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        deploy_railway()
    elif choice == "2":
        deploy_render()
    elif choice == "3":
        deploy_heroku()
    elif choice == "4":
        deploy_digitalocean()
    elif choice == "5":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice. Please try again.")
        show_deployment_options()

def deploy_railway():
    print("\n🚂 Railway Deployment Guide:")
    print("=" * 40)
    print("1. Go to https://railway.app and sign up")
    print("2. Click 'New Project' → 'Deploy from GitHub repo'")
    print("3. Connect your GitHub account")
    print("4. Select this repository")
    print("5. Railway will automatically detect Python and deploy")
    print("6. Add PostgreSQL database from Railway dashboard")
    print("7. Set environment variable: DATABASE_URL=your_postgres_url")
    print("\n✅ Your API will be live at: https://your-app-name.railway.app")
    print("📖 API docs: https://your-app-name.railway.app/docs")

def deploy_render():
    print("\n🎨 Render Deployment Guide:")
    print("=" * 40)
    print("1. Go to https://render.com and sign up")
    print("2. Click 'New' → 'Web Service'")
    print("3. Connect your GitHub repository")
    print("4. Configure:")
    print("   - Name: genhealth-api")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT")
    print("5. Add PostgreSQL database")
    print("6. Set environment variable: DATABASE_URL=your_postgres_url")
    print("\n✅ Your API will be live at: https://your-app-name.onrender.com")

def deploy_heroku():
    print("\n⚡ Heroku Deployment Guide:")
    print("=" * 40)
    print("1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
    print("2. Run these commands:")
    print("   heroku login")
    print("   heroku create your-genhealth-api")
    print("   heroku addons:create heroku-postgresql:mini")
    print("   git add .")
    print("   git commit -m 'Deploy to Heroku'")
    print("   git push heroku main")
    print("\n✅ Your API will be live at: https://your-app-name.herokuapp.com")

def deploy_digitalocean():
    print("\n🌊 DigitalOcean Deployment Guide:")
    print("=" * 40)
    print("1. Go to https://digitalocean.com and sign up")
    print("2. Click 'Create' → 'Apps'")
    print("3. Connect your GitHub repository")
    print("4. Configure build and run commands")
    print("5. Add database if needed")
    print("6. Deploy")
    print("\n✅ Your API will be live at your DigitalOcean app URL")

def create_procfile():
    """Create Procfile for Heroku deployment"""
    if not os.path.exists("Procfile"):
        with open("Procfile", "w") as f:
            f.write("web: uvicorn app.main:app --host 0.0.0.0 --port $PORT\n")
        print("✅ Created Procfile for Heroku deployment")

def main():
    print_header()
    
    if not check_requirements():
        print("\n❌ Please fix missing files before deploying")
        sys.exit(1)
    
    # Create Procfile for Heroku
    create_procfile()
    
    print("\n🎯 Your API is ready for deployment!")
    print("📁 Files to be deployed:")
    for file in os.listdir("."):
        if file.endswith((".py", ".txt", ".md")) or file in ["app", "Procfile"]:
            print(f"   ✅ {file}")
    
    show_deployment_options()

if __name__ == "__main__":
    main() 