#!/usr/bin/env python3
"""
Fixed Face Recognition Module - Proper name retrieval from database
"""

import cv2
import face_recognition
import pickle
import os
import numpy as np
from datetime import datetime

ENCODINGS_FILE = "face_encodings.pkl"

class FixedFaceRecognizer:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.known_metadata = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces with proper name association - FIXED VERSION"""
        if not os.path.exists(ENCODINGS_FILE):
            print("❌ No registered faces found!")
            print("💡 Please register faces first using fixed_register_face.py")
            return False
        
        try:
            with open(ENCODINGS_FILE, "rb") as f:
                known_data = pickle.load(f)
            
            if not known_data:
                print("❌ No face data found in encodings file!")
                return False
            
            # Clear existing data
            self.known_encodings = []
            self.known_names = []
            self.known_metadata = []
            
            print(f"📂 Loading {len(known_data)} face records...")
            
            # Load face data with proper validation
            for i, entry in enumerate(known_data):
                if isinstance(entry, dict):
                    # Check for required fields
                    if "encoding" in entry and "name" in entry:
                        name = entry["name"]
                        encoding = entry["encoding"]
                        
                        # Validate encoding format
                        if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
                            self.known_encodings.append(encoding)
                            self.known_names.append(name)
                            self.known_metadata.append(entry)
                            print(f"   ✅ Loaded: {name} (ID: {entry.get('id', 'unknown')})")
                        else:
                            print(f"   ❌ Invalid encoding for {name}")
                    else:
                        print(f"   ❌ Missing name or encoding in entry {i}")
                else:
                    print(f"   ❌ Invalid entry format at index {i}")
            
            print(f"✅ Successfully loaded {len(self.known_names)} known faces:")
            for i, name in enumerate(self.known_names):
                print(f"   {i+1}. {name}")
            
            return len(self.known_names) > 0
            
        except Exception as e:
            print(f"❌ Error loading known faces: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def recognize_face_with_correct_name(self, face_encoding):
        """Fixed face recognition that returns the correct registered name"""
        if not self.known_encodings:
            return "Unknown", 0.0, 1.0
        
        try:
            # Calculate distances to all known faces
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            
            # Find the best match
            best_match_index = np.argmin(face_distances)
            best_distance = face_distances[best_match_index]
            
            # Calculate confidence percentage
            confidence = max(0, (1 - best_distance) * 100)
            
            # Use stricter matching criteria for accuracy
            tolerance = 0.45  # Stricter tolerance
            min_confidence = 60.0  # Minimum confidence
            
            # Check if the match is good enough
            if best_distance <= tolerance and confidence >= min_confidence:
                # Get the correct name from our loaded data
                recognized_name = self.known_names[best_match_index]
                
                print(f"✅ RECOGNIZED: {recognized_name}")
                print(f"   Confidence: {confidence:.1f}%")
                print(f"   Distance: {best_distance:.3f}")
                print(f"   Match Index: {best_match_index}")
                
                return recognized_name, confidence, best_distance
            else:
                print(f"❓ No confident match found")
                print(f"   Best candidate: {self.known_names[best_match_index] if self.known_names else 'None'}")
                print(f"   Confidence: {confidence:.1f}%")
                print(f"   Distance: {best_distance:.3f}")
                
                return "Unknown", confidence, best_distance
                
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            import traceback
            traceback.print_exc()
            return "Unknown", 0.0, 1.0
    
    def recognize_faces_realtime(self):
        """Real-time face recognition with correct name display"""
        if not self.known_encodings:
            print("❌ No known faces loaded! Please register faces first.")
            return False
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access camera!")
            return False
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("\n" + "="*50)
        print("🎯 FIXED FACE RECOGNITION - CORRECT NAMES")
        print("="*50)
        print("📹 Camera started - Press 'Q' to quit, 'R' to reload faces")
        print(f"🔍 Ready to recognize {len(self.known_names)} registered faces:")
        for i, name in enumerate(self.known_names):
            print(f"   {i+1}. {name}")
        print("-" * 50)
        
        # Performance optimization
        process_this_frame = True
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Camera error!")
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            # Process every other frame for better performance
            if process_this_frame:
                # Resize for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find faces and encodings
                face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=1)
                
                face_names = []
                face_confidences = []
                
                for face_encoding in face_encodings:
                    # Use fixed recognition method
                    name, confidence, distance = self.recognize_face_with_correct_name(face_encoding)
                    face_names.append(name)
                    face_confidences.append(confidence)
            
            process_this_frame = not process_this_frame
            
            # Display results
            for (top, right, bottom, left), name, confidence in zip(face_locations, face_names, face_confidences):
                # Scale back up face locations
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                
                # Choose color based on recognition
                if name == "Unknown":
                    color = (0, 0, 255)  # Red for unknown
                    label_color = (255, 255, 255)
                    label = "Unknown"
                else:
                    color = (0, 255, 0)  # Green for recognized
                    label_color = (0, 0, 0)
                    label = f"{name} ({confidence:.1f}%)"
                
                # Draw rectangle around face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw label background
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
                cv2.rectangle(frame, (left, bottom - 35), (left + label_size[0], bottom), color, cv2.FILLED)
                
                # Draw label text
                cv2.putText(frame, label, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, label_color, 1)
            
            # Add status information
            status = f"Registered: {len(self.known_names)} | Detected: {len(face_locations)}"
            cv2.putText(frame, status, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow("Fixed Face Recognition - Press 'Q' to Quit, 'R' to Reload", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('r') or key == ord('R'):
                print("🔄 Reloading known faces...")
                self.load_known_faces()
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n📊 Session completed after {frame_count} frames")
        print("✅ Face recognition stopped.")
        return True

def recognize_faces():
    """Main function for fixed face recognition"""
    recognizer = FixedFaceRecognizer()
    if recognizer.known_encodings:
        return recognizer.recognize_faces_realtime()
    else:
        print("❌ No faces registered. Please register faces first using fixed_register_face.py")
        return False

def debug_face_database():
    """Debug function to check the face database"""
    print("\n🔍 DEBUGGING FACE DATABASE")
    print("=" * 40)
    
    if not os.path.exists(ENCODINGS_FILE):
        print("❌ No encodings file found!")
        return
    
    try:
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
        
        print(f"📊 Total entries in database: {len(data)}")
        print("\n📋 Database contents:")
        
        for i, entry in enumerate(data):
            print(f"\nEntry {i+1}:")
            if isinstance(entry, dict):
                print(f"   Name: {entry.get('name', 'MISSING')}")
                print(f"   ID: {entry.get('id', 'MISSING')}")
                print(f"   Timestamp: {entry.get('timestamp', 'MISSING')}")
                print(f"   Has encoding: {'Yes' if 'encoding' in entry else 'NO'}")
                if 'encoding' in entry:
                    enc = entry['encoding']
                    if isinstance(enc, np.ndarray):
                        print(f"   Encoding shape: {enc.shape}")
                    else:
                        print(f"   Encoding type: {type(enc)}")
            else:
                print(f"   Invalid entry type: {type(entry)}")
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        debug_face_database()
    else:
        recognize_faces()