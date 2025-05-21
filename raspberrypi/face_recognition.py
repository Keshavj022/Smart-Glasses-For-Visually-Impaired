import cv2
import numpy as np
import os
import pickle
import face_recognition

class FaceRecognizer:
    def __init__(self, config):
        self.known_face_encodings = []
        self.known_face_names = []
        self.config = config
        
        # Load known faces
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from the database"""
        faces_dir = 'faces'
        
        # Create directory if it doesn't exist
        if not os.path.exists(faces_dir):
            os.makedirs(faces_dir)
            return
        
        # Try to load from pickle file for efficiency
        pickle_path = os.path.join(faces_dir, 'known_faces.pkl')
        if os.path.exists(pickle_path):
            with open(pickle_path, 'rb') as f:
                data = pickle.load(f)
                self.known_face_encodings = data['encodings']
                self.known_face_names = data['names']
            return
        
        # Otherwise, load each image and compute encodings
        for filename in os.listdir(faces_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                path = os.path.join(faces_dir, filename)
                name = os.path.splitext(filename)[0]
                
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)
                
                if len(encoding) > 0:
                    self.known_face_encodings.append(encoding[0])
                    self.known_face_names.append(name)
        
        # Save to pickle for future use
        with open(pickle_path, 'wb') as f:
            pickle.dump({
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }, f)
    
    def identify_faces(self, frame):
        """Identify faces in the frame"""
        if frame is None:
            return []
        
        # Convert BGR to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all face locations and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        results = []
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = 0.0
            
            # Find the best match
            if len(self.known_face_encodings) > 0:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                confidence = 1 - face_distances[best_match_index]
                
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            
            results.append({
                'name': name,
                'confidence': confidence,
                'location': (top, right, bottom, left)
            })
        
        return results
    
    def add_new_face(self, frame, name):
        """Add a new face to the database"""
        if frame is None:
            return False
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) != 1:
            return False  # Require exactly one face
        
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        if len(face_encodings) == 0:
            return False
        
        # Add to known faces
        self.known_face_encodings.append(face_encodings[0])
        self.known_face_names.append(name)
        
        # Save face image
        faces_dir = 'faces'
        if not os.path.exists(faces_dir):
            os.makedirs(faces_dir)
        
        # Extract face from frame and save
        top, right, bottom, left = face_locations[0]
        face_image = frame[top:bottom, left:right]
        cv2.imwrite(os.path.join(faces_dir, f"{name}.jpg"), face_image)
        
        # Update pickle file
        pickle_path = os.path.join(faces_dir, 'known_faces.pkl')
        with open(pickle_path, 'wb') as f:
            pickle.dump({
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }, f)
        
        return True
