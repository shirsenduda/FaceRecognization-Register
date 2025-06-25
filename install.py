#!/usr/bin/env python3
"""
Installation and setup script for Face Recognition System
"""

import subprocess
import sys
import os
import platform

def print_header():
    print("="*60)
    print("🎭 Face Recognition System - Installation Script")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_system_dependencies():
    """Install system-level dependencies"""
    print("\n🔧 Checking system dependencies...")
    
    system = platform.system().lower()
    
    if system == "linux":
        print("📋 Linux detected - Please install these packages if not already installed:")
        print("   sudo apt-get update")
        print("   sudo apt-get install build-essential cmake")
        print("   sudo apt-get install libopenblas-dev liblapack-dev")
        print("   sudo apt-get install libx11-dev libgtk-3-dev")
        print("   sudo apt-get install python3-dev")
        
    elif system == "darwin":  # macOS
        print("🍎 macOS detected - Please install Xcode command line tools:")
        print("   xcode-select --install")
        
    elif system == "windows":
        print("🪟 Windows detected - Visual Studio Build Tools may be required")
        print("   Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    
    input("Press Enter after installing system dependencies (or if already installed)...")

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python packages...")
    
    try:
        # Ensure pip is up to date
        print("🔄 Updating pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        if os.path.exists("requirements.txt"):
            print("📋 Installing from requirements.txt...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            print("📋 Installing individual packages...")
            packages = [
                "opencv-python>=4.8.0",
                "face-recognition>=1.3.0",
                "dlib>=19.24.0",
                "Pillow>=10.0.0",
                "numpy>=1.24.0",
                "pandas>=2.0.0",
                "openpyxl>=3.1.0",
                "colorama>=0.4.6",
                "Flask>=2.3.0",
                "Flask-CORS>=4.0.0"
            ]
            
            for package in packages:
                print(f"   Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["registered_faces", "logs", "backups"]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True

def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    test_imports = [
        ("cv2", "OpenCV"),
        ("face_recognition", "Face Recognition"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("PIL", "Pillow"),
        ("flask", "Flask")
    ]
    
    failed_imports = []
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n❌ Some imports failed: {', '.join(failed_imports)}")
        return False
    
    print("\n✅ All imports successful!")
    return True

def create_config_file():
    """Create a configuration file"""
    print("\n⚙️ Creating configuration file...")
    
    config_content = """# Face Recognition System Configuration
# Edit these settings as needed

[RECOGNITION]
# Recognition tolerance (lower = stricter matching)
tolerance = 0.45

# Minimum confidence percentage for recognition
min_confidence = 50.0

# Face encoding model (small/large)
encoding_model = large

# Number of jitters for encoding (higher = better quality, slower)
num_jitters = 10

[FILES]
# Directory for storing registered face images
register_dir = registered_faces

# Excel file for user registration log
excel_file = registered_users.xlsx

# Pickle file for face encodings
encodings_file = face_encodings.pkl

[SERVER]
# Flask server settings
host = 0.0.0.0
port = 5000
debug = False
"""
    
    try:
        with open("config.ini", "w") as f:
            f.write(config_content)
        print("✅ Configuration file created: config.ini")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def main():
    """Main installation function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python requirements
    if not install_requirements():
        print("\n❌ Installation failed!")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Directory creation failed!")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed!")
        sys.exit(1)
    
    # Create config file
    create_config_file()
    
    print("\n" + "="*60)
    print("🎉 Installation completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Run 'python main.py' to start the system")
    print("2. Or run 'python app.py' to start the web backend")
    print("3. Register faces using option 1 in the menu")
    print("4. Test recognition using option 2 in the menu")
    print("\n💡 Tips:")
    print("• Ensure good lighting when registering/recognizing faces")
    print("• Register multiple angles of the same person for better accuracy")
    print("• Keep faces clear and well-positioned in the camera view")
    print("\n🔧 Configuration:")
    print("• Edit 'config.ini' to adjust recognition settings")
    print("• Check 'requirements.txt' for package versions")
    print("\n✅ System ready to use!")

if __name__ == "__main__":
    main()