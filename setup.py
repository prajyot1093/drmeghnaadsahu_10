#!/usr/bin/env python3
"""
Setup script for the Unified Service Management Portal
Run this to prepare the application for first use
"""

import os
import sys
import subprocess

def setup_environment():
    """Setup the development environment"""
    
    print("=" * 60)
    print("Unified Service Management Portal - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Create virtual environment
    print("\n📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to create virtual environment")
    
    # Install requirements
    print("\n📥 Installing dependencies...")
    pip_path = os.path.join("venv", "Scripts", "pip") if os.name == 'nt' else os.path.join("venv", "bin", "pip")
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Initialize database
    print("\n🗄️  Initializing database...")
    python_path = os.path.join("venv", "Scripts", "python") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    
    try:
        subprocess.run([python_path, "init_app.py"], check=True)
        print("✅ Database initialized")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to initialize database")
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    
    print("\n📝 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Run the application:")
    print("   streamlit run app.py")
    
    print("\n3. Login with demo credentials:")
    print("   Student: student@example.com / student123")
    print("   Admin: admin@example.com / admin123")

if __name__ == "__main__":
    setup_environment()
