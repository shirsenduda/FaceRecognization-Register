#!/usr/bin/env python3
"""
Fixed GUI Application - Proper name handling and database connection
"""

import tkinter as tk
from tkinter import messagebox, ttk
import cv2
from PIL import Image, ImageTk
import threading
import os
from fixed_register_face import register_user_fixed, list_registered_users
from fixed_recognize_face import recognize_faces, debug_face_database

class FixedFaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fixed Face Recognition System")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main title
        title_label = tk.Label(
            root, 
            text="🎭 Fixed Face Recognition System", 
            font=("Arial", 20, "bold"),
            fg="#2E4057",
            bg="#F0F0F0"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            root,
            text="Proper Database Connection - Names Display Correctly",
            font=("Arial", 12),
            fg="#666666",
            bg="#F0F0F0"
        )
        subtitle_label.pack(pady=5)
        
        # Create main frame
        main_frame = tk.Frame(root, bg="#F0F0F0")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Registration section
        reg_frame = tk.LabelFrame(
            main_frame,
            text="👤 Face Registration",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=15,
            bg="#E8F4FD",
            fg="#2E4057"
        )
        reg_frame.pack(fill="x", pady=10)
        
        # Name input
        tk.Label(
            reg_frame,
            text="Enter Your Name:",
            font=("Arial", 12),
            bg="#E8F4FD"
        ).pack(anchor="w", pady=(0, 5))
        
        self.name_entry = tk.Entry(
            reg_frame,
            width=40,
            font=("Arial", 12),
            relief="solid",
            borderwidth=1
        )
        self.name_entry.pack(pady=(0, 10))
        
        # Register button
        self.register_btn = tk.Button(
            reg_frame,
            text="📷 Register Face",
            command=self.register_face_fixed,
            width=25,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.register_btn.pack(pady=5)
        
        # Recognition section
        rec_frame = tk.LabelFrame(
            main_frame,
            text="🔍 Face Recognition",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=15,
            bg="#FFF3E0",
            fg="#2E4057"
        )
        rec_frame.pack(fill="x", pady=10)
        
        # Recognition button
        self.recognize_btn = tk.Button(
            rec_frame,
            text="🚀 Start Face Recognition",
            command=self.start_recognition_fixed,
            width=25,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.recognize_btn.pack(pady=5)
        
        # Status section
        status_frame = tk.LabelFrame(
            main_frame,
            text="📊 System Status",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=15,
            bg="#F3E5F5",
            fg="#2E4057"
        )
        status_frame.pack(fill="x", pady=10)
        
        # Status buttons frame
        status_btn_frame = tk.Frame(status_frame, bg="#F3E5F5")
        status_btn_frame.pack()
        
        # List users button
        self.list_btn = tk.Button(
            status_btn_frame,
            text="👥 List Users",
            command=self.list_users,
            width=15,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.list_btn.pack(side="left", padx=5)
        
        # Debug button
        self.debug_btn = tk.Button(
            status_btn_frame,
            text="🔍 Debug DB",
            command=self.debug_database,
            width=15,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.debug_btn.pack(side="left", padx=5)
        
        # Status display
        self.status_text = tk.Text(
            status_frame,
            height=8,
            width=70,
            font=("Consolas", 9),
            bg="#FAFAFA",
            fg="#333333",
            relief="solid",
            borderwidth=1
        )
        self.status_text.pack(pady=10)
        
        # Scrollbar for status text
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Exit button
        self.quit_btn = tk.Button(
            main_frame,
            text="🚪 Exit",
            command=self.root.quit,
            width=20,
            height=2,
            bg="#F44336",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.quit_btn.pack(pady=20)
        
        # Initialize status
        self.update_status("✅ Fixed Face Recognition System initialized")
        self.update_status("📋 This version properly connects names to face database")
        self.check_database_status()
    
    def update_status(self, message):
        """Update status display"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def check_database_status(self):
        """Check and display database status"""
        try:
            if os.path.exists("face_encodings.pkl"):
                import pickle
                with open("face_encodings.pkl", "rb") as f:
                    data = pickle.load(f)
                count = len(data)
                self.update_status(f"📊 Database Status: {count} faces registered")
                
                # Show registered names
                names = [entry.get("name", "Unknown") for entry in data if isinstance(entry, dict)]
                if names:
                    self.update_status(f"👥 Registered users: {', '.join(names[:5])}")
                    if len(names) > 5:
                        self.update_status(f"    ... and {len(names)-5} more")
            else:
                self.update_status("📊 Database Status: No faces registered yet")
        except Exception as e:
            self.update_status(f"⚠️  Database check error: {e}")
    
    def register_face_fixed(self):
        """Fixed registration with proper name handling"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name first!")
            return
        
        if len(name) < 2:
            messagebox.showerror("Error", "Name must be at least 2 characters long!")
            return
        
        self.update_status(f"🚀 Starting registration for: {name}")
        self.register_btn.config(state="disabled")
        
        # Run registration in thread
        thread = threading.Thread(target=self.register_thread, args=(name,))
        thread.daemon = True
        thread.start()
    
    def register_thread(self, name):
        """Registration thread with proper error handling"""
        try:
            self.update_status(f"📷 Opening camera for {name}...")
            success = register_user_fixed(name)
            
            if success:
                self.update_status(f"✅ SUCCESS: Face registered for {name}")
                messagebox.showinfo("Success", f"Face registered successfully for {name}!")
                self.name_entry.delete(0, tk.END)
                self.check_database_status()
            else:
                self.update_status(f"❌ FAILED: Registration failed for {name}")
                messagebox.showerror("Error", f"Registration failed for {name}")
            
        except Exception as e:
            self.update_status(f"❌ ERROR: {e}")
            messagebox.showerror("Error", f"Registration error: {e}")
        
        finally:
            self.register_btn.config(state="normal")
    
    def start_recognition_fixed(self):
        """Fixed recognition with proper name display"""
        self.update_status("🎯 Starting fixed face recognition...")
        self.recognize_btn.config(state="disabled")
        
        # Run recognition in thread
        thread = threading.Thread(target=self.recognition_thread)
        thread.daemon = True
        thread.start()
    
    def recognition_thread(self):
        """Recognition thread"""
        try:
            self.update_status("📹 Opening camera for recognition...")
            success = recognize_faces()
            
            if success:
                self.update_status("✅ Recognition session completed")
            else:
                self.update_status("❌ Recognition failed to start")
                messagebox.showerror("Error", "Recognition failed. Please register faces first.")
            
        except Exception as e:
            self.update_status(f"❌ Recognition error: {e}")
            messagebox.showerror("Error", f"Recognition error: {e}")
        
        finally:
            self.recognize_btn.config(state="normal")
    
    def list_users(self):
        """List registered users"""
        self.update_status("📋 Listing registered users...")
        try:
            list_registered_users()
            self.update_status("✅ User list displayed in console")
        except Exception as e:
            self.update_status(f"❌ Error listing users: {e}")
    
    def debug_database(self):
        """Debug database contents"""
        self.update_status("🔍 Running database debug...")
        try:
            debug_face_database()
            self.update_status("✅ Database debug completed - check console")
        except Exception as e:
            self.update_status(f"❌ Debug error: {e}")

def main():
    """Main application entry point"""
    print("🚀 Starting Fixed Face Recognition GUI...")
    print("=" * 50)
    print("✅ This version fixes the name-database connection issue")
    print("📋 Names will now display correctly during recognition")
    print("=" * 50)
    
    # Check dependencies
    try:
        import cv2
        import face_recognition
        import pandas as pd
        import numpy as np
        print("✅ All dependencies loaded successfully")
    except ImportError as e:
        print(f"❌ Dependency error: {e}")
        print("   Please install: pip install opencv-python face-recognition pandas numpy pillow")
        return
    
    # Create and run GUI
    root = tk.Tk()
    root.configure(bg="#F0F0F0")
    app = FixedFaceApp(root)
    
    print("🎭 GUI launched - ready for use!")
    root.mainloop()

if __name__ == "__main__":
    main()