#!/usr/bin/env python3
"""
Fixed Face Recognition Backend - Proper name storage and retrieval
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import face_recognition
import pickle
import os
import pandas as pd
import uuid
from datetime import datetime
import numpy as np
import traceback
import json

# Create Flask app
app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Constants
REGISTER_DIR = "registered_faces"
EXCEL_FILE = "registered_users.xlsx"
ENCODINGS_FILE = "face_encodings.pkl"

# Ensure directories exist
os.makedirs(REGISTER_DIR, exist_ok=True)

class FixedFaceRecognitionSystem:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.known_metadata = []
        self.load_known_faces()
        
        # Recognition settings
        self.tolerance = 0.45
        self.min_confidence = 60.0
    
    def load_known_faces(self):
        """Load known faces with proper name association"""
        self.known_encodings = []
        self.known_names = []
        self.known_metadata = []
        
        if os.path.exists(ENCODINGS_FILE):
            try:
                with open(ENCODINGS_FILE, "rb") as f:
                    known_data = pickle.load(f)
                
                print(f"📂 Loading {len(known_data)} face records...")
                
                for i, entry in enumerate(known_data):
                    if isinstance(entry, dict):
                        # Check if entry has required fields
                        if "encoding" in entry and "name" in entry:
                            name = entry["name"]
                            encoding = entry["encoding"]
                            
                            # Validate encoding
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
                
                print(f"✅ Successfully loaded {len(self.known_names)} valid faces")
                return True
                
            except Exception as e:
                print(f"❌ Error loading faces: {e}")
                traceback.print_exc()
                return False
        else:
            print("📝 No existing face database found")
            return False
    
    def save_face_data(self, name, encoding, image_path, unique_id):
        """Save face data with proper name association"""
        try:
            # Load existing data
            if os.path.exists(ENCODINGS_FILE):
                with open(ENCODINGS_FILE, "rb") as f:
                    data = pickle.load(f)
            else:
                data = []
            
            # Create new entry with all required fields
            new_entry = {
                "name": name,
                "encoding": encoding,
                "image_path": image_path,
                "id": unique_id,
                "timestamp": datetime.now().isoformat(),
                "quality": "high"
            }
            
            # Add to data
            data.append(new_entry)
            
            # Save back to file
            with open(ENCODINGS_FILE, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            print(f"💾 Saved face data for {name} with ID {unique_id}")
            
            # Also save to Excel for backup
            self.save_to_excel(name, unique_id, image_path)
            
            # Reload the known faces
            self.load_known_faces()
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving face data: {e}")
            traceback.print_exc()
            return False
    
    def save_to_excel(self, name, unique_id, image_path):
        """Save registration to Excel file"""
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
            print(f"📊 Excel updated for {name}")
            
        except Exception as e:
            print(f"⚠️ Excel update warning: {e}")
    
    def recognize_face_with_name(self, face_encoding):
        """Recognize face and return correct name"""
        if not self.known_encodings:
            return "Unknown", 0.0, 1.0
        
        try:
            # Calculate distances to all known faces
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            
            # Find best match
            best_match_index = np.argmin(face_distances)
            best_distance = face_distances[best_match_index]
            
            # Calculate confidence
            confidence = max(0, (1 - best_distance) * 100)
            
            # Check if match is good enough
            if best_distance <= self.tolerance and confidence >= self.min_confidence:
                recognized_name = self.known_names[best_match_index]
                
                print(f"✅ Recognized: {recognized_name} (confidence: {confidence:.1f}%, distance: {best_distance:.3f})")
                
                return recognized_name, confidence, best_distance
            else:
                print(f"❓ No match found (best: {self.known_names[best_match_index] if self.known_names else 'None'}, confidence: {confidence:.1f}%)")
                return "Unknown", confidence, best_distance
                
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            return "Unknown", 0.0, 1.0

# Initialize the system
face_system = FixedFaceRecognitionSystem()

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Fixed Face Recognition Backend Server',
        'status': 'running',
        'registered_faces': len(face_system.known_names),
        'endpoints': {
            'GET /api/status': 'Server status',
            'POST /api/register': 'Register new face',
            'POST /api/recognize': 'Recognize faces',
            'GET /api/users': 'List registered users'
        }
    })

@app.route('/api/status', methods=['GET', 'OPTIONS'])
def get_status():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        return jsonify({
            'status': 'connected',
            'message': 'Backend server running',
            'registered_faces': len(face_system.known_names),
            'database_loaded': len(face_system.known_encodings) > 0,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register_face():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("📥 Registration request received")
        
        # Get name from request
        name = request.form.get('name', '').strip()
        if not name:
            return jsonify({
                'success': False,
                'message': 'Name is required'
            }), 400
        
        print(f"👤 Registering face for: {name}")
        
        # Get image file
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file provided'
            }), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No image file selected'
            }), 400
        
        # Process image
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({
                'success': False,
                'message': 'Invalid image format'
            }), 400
        
        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        
        if len(face_locations) == 0:
            return jsonify({
                'success': False,
                'message': 'No face detected in image'
            }), 400
        
        if len(face_locations) > 1:
            return jsonify({
                'success': False,
                'message': 'Multiple faces detected. Please ensure only one face is visible'
            }), 400
        
        # Get face encoding
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=10)
        
        if len(face_encodings) == 0:
            return jsonify({
                'success': False,
                'message': 'Could not encode face'
            }), 400
        
        encoding = face_encodings[0]
        
        # Check for duplicates
        if face_system.known_encodings:
            face_distances = face_recognition.face_distance(face_system.known_encodings, encoding)
            if len(face_distances) > 0 and np.min(face_distances) < 0.4:
                min_index = np.argmin(face_distances)
                existing_name = face_system.known_names[min_index]
                return jsonify({
                    'success': False,
                    'message': f'Face already registered as "{existing_name}"'
                }), 400
        
        # Generate unique ID and save image
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{unique_id}_{timestamp}.jpg"
        image_path = os.path.join(REGISTER_DIR, filename)
        
        # Save image
        cv2.imwrite(image_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"💾 Image saved: {filename}")
        
        # Save face data with proper name association
        success = face_system.save_face_data(name, encoding, image_path, unique_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Face registered successfully for {name}',
                'user_id': unique_id,
                'registered_count': len(face_system.known_names)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save face data'
            }), 500
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@app.route('/api/recognize', methods=['POST', 'OPTIONS'])
def recognize_face():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("🔍 Recognition request received")
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file provided'
            }), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No image file selected'
            }), 400
        
        # Process image
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({
                'success': False,
                'message': 'Invalid image format'
            }), 400
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=5)
        
        recognized_faces = []
        
        for i, (face_encoding, face_location) in enumerate(zip(face_encodings, face_locations)):
            # Use fixed recognition with proper name retrieval
            name, confidence, distance = face_system.recognize_face_with_name(face_encoding)
            
            top, right, bottom, left = face_location
            
            recognized_faces.append({
                'name': name,
                'confidence': float(confidence),
                'distance': float(distance),
                'location': {
                    'top': int(top),
                    'right': int(right),
                    'bottom': int(bottom),
                    'left': int(left)
                }
            })
        
        return jsonify({
            'success': True,
            'faces': recognized_faces,
            'total_faces': len(recognized_faces),
            'known_faces': len([f for f in recognized_faces if f['name'] != 'Unknown'])
        })
        
    except Exception as e:
        print(f"❌ Recognition error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Recognition failed: {str(e)}'
        }), 500

@app.route('/api/users', methods=['GET', 'OPTIONS'])
def list_users():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        users = []
        for i, (name, metadata) in enumerate(zip(face_system.known_names, face_system.known_metadata)):
            users.append({
                'id': metadata.get('id', f'user_{i}'),
                'name': name,
                'timestamp': metadata.get('timestamp', 'Unknown'),
                'image_path': metadata.get('image_path', '')
            })
        
        return jsonify({
            'success': True,
            'users': users,
            'total_users': len(users)
        })
        
    except Exception as e:
        print(f"❌ Error listing users: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Fixed Face Recognition Backend...")
    print("=" * 50)
    print(f"📍 Backend URL: http://localhost:5000")
    print(f"📂 Registered faces: {len(face_system.known_names)}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)