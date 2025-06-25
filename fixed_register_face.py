#!/usr/bin/env python3
"""
Fixed Face Registration Module - Proper name handling
"""

import cv2
import face_recognition
import os
import pandas as pd
import uuid
from datetime import datetime
import pickle
import numpy as np

REGISTER_DIR = "registered_faces"
EXCEL_FILE = "registered_users.xlsx"
ENCODINGS_FILE = "face_encodings.pkl"

# Create directories if they don't exist
os.makedirs(REGISTER_DIR, exist_ok=True)

def register_user_fixed(name=None):
    """Fixed registration function that properly handles names"""
    print("\n" + "="*50)
    print("🎭 FIXED FACE REGISTRATION SYSTEM")
    print("="*50)
    
    # Get name parameter or ask for input
    if name is None:
        name = input("👤 Enter your name: ").strip()
    else:
        print(f"👤 Registering face for: {name}")
    
    if not name:
        print("❌ Name cannot be empty!")
        return False
        
    if len(name) < 2:
        print("❌ Name must be at least 2 characters long!")
        return False
    
    # Check if name already exists
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            if name.lower() in df['Name'].str.lower().values:
                print(f"⚠️  Name '{name}' already exists!")
                choice = input("Do you want to register anyway? (y/N): ").strip().lower()
                if choice != 'y':
                    return False
        except Exception as e:
            print(f"⚠️  Warning: Could not check existing names: {e}")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot access camera!")
        return False
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print(f"\n📹 Camera started for '{name}'")
    print("📋 Instructions:")
    print("   • Position your face clearly in the camera view")
    print("   • Ensure good lighting")
    print("   • Make sure only YOUR face is visible")
    print("   • Press 'S' to capture your face")
    print("   • Press 'Q' to quit")
    print("-" * 50)
    
    face_captured = False
    attempts = 0
    max_attempts = 5
    
    while not face_captured and attempts < max_attempts:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera error!")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB for face detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        
        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (left, top-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Add status text
        status_text = f"Faces: {len(face_locations)} | Press 'S' to capture"
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, f"Registering: {name}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("Face Registration - Press 'S' to Save, 'Q' to Quit", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s') or key == ord('S'):
            attempts += 1
            print(f"\n🔍 Capture attempt {attempts}/{max_attempts}")
            
            if len(face_locations) == 0:
                print("❌ No face detected! Please position yourself in the camera view.")
                continue
            elif len(face_locations) > 1:
                print("❌ Multiple faces detected! Please ensure only one face is visible.")
                continue
            
            # Single face detected - proceed with encoding
            print("✅ Single face detected! Processing...")
            
            try:
                # Get face encodings with higher accuracy
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=10, model="large")
                
                if len(face_encodings) == 0:
                    print("❌ Could not encode face. Please try again with better lighting.")
                    continue
                
                encoding = face_encodings[0]
                print("✅ Face encoded successfully!")
                
                # Check for duplicates
                if os.path.exists(ENCODINGS_FILE):
                    try:
                        with open(ENCODINGS_FILE, "rb") as f:
                            existing_data = pickle.load(f)
                        
                        existing_encodings = [entry["encoding"] for entry in existing_data if "encoding" in entry]
                        
                        if existing_encodings:
                            matches = face_recognition.compare_faces(existing_encodings, encoding, tolerance=0.4)
                            
                            if True in matches:
                                match_index = matches.index(True)
                                existing_name = existing_data[match_index]["name"]
                                print(f"⚠️  This face appears to be already registered as '{existing_name}'")
                                choice = input("Continue with registration anyway? (y/N): ").strip().lower()
                                if choice != 'y':
                                    continue
                    except Exception as e:
                        print(f"⚠️  Warning: Could not check existing faces: {e}")
                
                # Generate unique ID and filename
                unique_id = str(uuid.uuid4())[:8]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{unique_id}_{timestamp}.jpg"
                image_path = os.path.join(REGISTER_DIR, filename)
                
                # Save the image
                if cv2.imwrite(image_path, frame):
                    print(f"💾 Image saved: {filename}")
                else:
                    print("❌ Failed to save image!")
                    continue
                
                # Save to Excel with proper name association
                success = save_to_excel(name, unique_id, image_path)
                if not success:
                    print("⚠️  Excel save failed, but continuing...")
                
                # Save face encoding with proper name association
                success = save_face_encoding(name, encoding, image_path, unique_id)
                
                if success:
                    print(f"\n✅ SUCCESS! Face registered for '{name}'")
                    print(f"👤 User ID: {unique_id}")
                    print(f"📸 Image: {filename}")
                    face_captured = True
                else:
                    print("❌ Failed to save face encoding!")
                    continue
                
            except Exception as e:
                print(f"❌ Error during face processing: {e}")
                continue
                
        elif key == ord('q') or key == ord('Q'):
            print("\n❌ Registration cancelled by user.")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if not face_captured and attempts >= max_attempts:
        print(f"\n❌ Registration failed after {max_attempts} attempts.")
        return False
    
    return face_captured

def save_to_excel(name, unique_id, image_path):
    """Save registration data to Excel with proper name association"""
    try:
        log_data = {
            "Name": name,
            "ID": unique_id,
            "Image": image_path,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "Active"
        }
        
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            df = pd.concat([df, pd.DataFrame([log_data])], ignore_index=True)
        else:
            df = pd.DataFrame([log_data])
        
        df.to_excel(EXCEL_FILE, index=False)
        print("📊 Excel file updated successfully!")
        return True
        
    except Exception as e:
        print(f"⚠️  Excel update failed: {e}")
        return False

def save_face_encoding(name, encoding, image_path, unique_id):
    """Save face encoding with proper name association"""
    try:
        # Load existing data
        if os.path.exists(ENCODINGS_FILE):
            with open(ENCODINGS_FILE, "rb") as f:
                data = pickle.load(f)
        else:
            data = []
        
        # Create new entry with proper name association
        encoding_data = {
            "name": name,  # This is the key fix - ensure name is properly stored
            "encoding": encoding,
            "image_path": image_path,
            "id": unique_id,
            "timestamp": datetime.now().isoformat(),
            "quality": "high"
        }
        
        # Add to data
        data.append(encoding_data)
        
        # Save with error checking
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        print("🔐 Face encoding saved successfully with name association!")
        
        # Verify the save worked
        verify_save(name, unique_id)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save face encoding: {e}")
        return False

def verify_save(name, unique_id):
    """Verify that the face data was saved correctly"""
    try:
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
        
        # Look for our entry
        for entry in data:
            if entry.get("id") == unique_id and entry.get("name") == name:
                print(f"✅ Verification successful: {name} data properly saved!")
                return True
        
        print(f"⚠️  Verification warning: Could not find saved data for {name}")
        return False
        
    except Exception as e:
        print(f"⚠️  Verification error: {e}")
        return False

def list_registered_users():
    """List all registered users with proper name display"""
    if not os.path.exists(ENCODINGS_FILE):
        print("📝 No registered users found.")
        return
    
    try:
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
        
        print(f"\n👥 Registered Users ({len(data)} total):")
        print("-" * 60)
        
        for idx, entry in enumerate(data):
            name = entry.get("name", "Unknown")
            user_id = entry.get("id", "N/A")
            timestamp = entry.get("timestamp", "Unknown")
            
            print(f"{idx+1:2d}. {name} (ID: {user_id}) - {timestamp}")
            
    except Exception as e:
        print(f"❌ Error reading user list: {e}")

if __name__ == "__main__":
    register_user_fixed()