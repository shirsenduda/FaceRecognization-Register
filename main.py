#!/usr/bin/env python3
"""
Enhanced Face Recognition System
Main entry point with improved user interface and error handling
"""

import os
import sys
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for cross-platform colored output
colorama.init()

def print_banner():
    """Print system banner"""
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + "🎭 ADVANCED FACE RECOGNITION SYSTEM")
    print(Fore.CYAN + "="*60)
    print(Fore.WHITE + "Version: 2.0 | Enhanced Accuracy & Performance")
    print(Fore.GREEN + f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.CYAN + "="*60 + Style.RESET_ALL)

def print_menu():
    """Print main menu"""
    print(Fore.WHITE + "\n📋 MAIN MENU:")
    print(Fore.GREEN + "1. 👤 Register New Face")
    print(Fore.BLUE + "2. 🔍 Start Face Recognition")
    print(Fore.YELLOW + "3. 👥 List Registered Users")
    print(Fore.MAGENTA + "4. 🧪 Test Recognition System")
    print(Fore.CYAN + "5. 📊 View System Status")
    print(Fore.RED + "6. 🚪 Exit")
    print(Fore.WHITE + "-" * 40 + Style.RESET_ALL)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'cv2': 'opencv-python',
        'face_recognition': 'face-recognition',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'PIL': 'Pillow'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(Fore.RED + "❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print(Fore.YELLOW + "\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        print(Style.RESET_ALL)
        return False
    
    return True

def check_system_files():
    """Check system file status"""
    files_to_check = {
        'register_face.py': 'Face registration module',
        'recognize.py': 'Face recognition module'
    }
    
    print(Fore.CYAN + "\n📁 System Files Status:")
    all_files_exist = True
    
    for filename, description in files_to_check.items():
        if os.path.exists(filename):
            print(Fore.GREEN + f"   ✅ {filename} - {description}")
        else:
            print(Fore.RED + f"   ❌ {filename} - {description} (MISSING)")
            all_files_exist = False
    
    # Check data files
    data_files = {
        'face_encodings.pkl': 'Face encodings database',
        'registered_users.xlsx': 'User registration log',
        'registered_faces/': 'Face images directory'
    }
    
    print(Fore.CYAN + "\n📊 Data Files Status:")
    for filename, description in data_files.items():
        if os.path.exists(filename):
            if filename.endswith('/'):
                # Directory
                count = len([f for f in os.listdir(filename) if f.endswith(('.jpg', '.png', '.jpeg'))])
                print(Fore.GREEN + f"   ✅ {filename} - {description} ({count} images)")
            else:
                print(Fore.GREEN + f"   ✅ {filename} - {description}")
        else:
            print(Fore.YELLOW + f"   ⚠️  {filename} - {description} (Not created yet)")
    
    print(Style.RESET_ALL)
    return all_files_exist

def get_system_stats():
    """Get and display system statistics"""
    print(Fore.CYAN + "\n📊 SYSTEM STATISTICS:")
    print(Fore.CYAN + "-" * 30)
    
    # Count registered faces
    registered_count = 0
    if os.path.exists('face_encodings.pkl'):
        try:
            import pickle
            with open('face_encodings.pkl', 'rb') as f:
                data = pickle.load(f)
            registered_count = len(data)
        except:
            registered_count = 0
    
    # Count image files
    image_count = 0
    if os.path.exists('registered_faces'):
        image_files = [f for f in os.listdir('registered_faces') 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        image_count = len(image_files)
    
    # Count Excel entries
    excel_count = 0
    if os.path.exists('registered_users.xlsx'):
        try:
            import pandas as pd
            df = pd.read_excel('registered_users.xlsx')
            excel_count = len(df)
        except:
            excel_count = 0
    
    print(Fore.GREEN + f"👤 Registered Faces: {registered_count}")
    print(Fore.BLUE + f"📸 Stored Images: {image_count}")
    print(Fore.YELLOW + f"📊 Excel Entries: {excel_count}")
    
    # Check data consistency
    if registered_count == image_count == excel_count:
        print(Fore.GREEN + "✅ Data consistency: GOOD")
    else:
        print(Fore.YELLOW + "⚠️  Data consistency: CHECK NEEDED")
    
    print(Style.RESET_ALL)

def main():
    """Main application loop"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print(Fore.RED + "❌ System check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Check system files
    if not check_system_files():
        print(Fore.RED + "❌ Missing critical system files.")
        sys.exit(1)
    
    print(Fore.GREEN + "✅ System check passed!" + Style.RESET_ALL)
    
    while True:
        try:
            print_menu()
            choice = input(Fore.WHITE + "Enter your choice (1-6): " + Style.RESET_ALL).strip()
            
            if choice == '1':
                print(Fore.YELLOW + "\n🚀 Starting face registration..." + Style.RESET_ALL)
                try:
                    from fixed_register_face import register_user
                    success = register_user()
                    if success:
                        print(Fore.GREEN + "✅ Registration completed successfully!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "❌ Registration failed or cancelled." + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"❌ Registration error: {e}" + Style.RESET_ALL)
            
            elif choice == '2':
                print(Fore.YELLOW + "\n🚀 Starting face recognition..." + Style.RESET_ALL)
                try:
                    from recognize import recognize_faces
                    success = recognize_faces()
                    if success:
                        print(Fore.GREEN + "✅ Recognition session completed!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "❌ Recognition failed to start." + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"❌ Recognition error: {e}" + Style.RESET_ALL)
            
            elif choice == '3':
                print(Fore.YELLOW + "\n📋 Listing registered users..." + Style.RESET_ALL)
                try:
                    from fixed_register_face import list_registered_users
                    list_registered_users()
                except Exception as e:
                    print(Fore.RED + f"❌ Error listing users: {e}" + Style.RESET_ALL)
            
            elif choice == '4':
                print(Fore.YELLOW + "\n🧪 Testing recognition system..." + Style.RESET_ALL)
                try:
                    from recognize import test_recognition
                    test_recognition()
                except Exception as e:
                    print(Fore.RED + f"❌ Test error: {e}" + Style.RESET_ALL)
            
            elif choice == '5':
                get_system_stats()
            
            elif choice == '6':
                print(Fore.CYAN + "\n👋 Thank you for using Face Recognition System!")
                print(Fore.YELLOW + "🎯 System shutting down..." + Style.RESET_ALL)
                break
            
            else:
                print(Fore.RED + "❌ Invalid choice. Please select 1-6." + Style.RESET_ALL)
        
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n⚠️  Interrupted by user. Shutting down..." + Style.RESET_ALL)
            break
        except Exception as e:
            print(Fore.RED + f"\n❌ Unexpected error: {e}" + Style.RESET_ALL)
            print(Fore.YELLOW + "💡 Please try again or restart the application." + Style.RESET_ALL)

if __name__ == "__main__":
    main()