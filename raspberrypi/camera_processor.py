import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

class CameraProcessor:
    def __init__(self):
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        
        # Load object detection model (using TensorFlow's SSD MobileNet)
        self.detect_fn = self.load_model()
        
        # Load label map
        self.category_index = self.load_labels()
        
    def load_model(self):
        """Load the object detection model"""
        # Path to saved model directory
        PATH_TO_MODEL_DIR = 'models/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
        
        # Load saved model and build detection function
        model = tf.saved_model.load(PATH_TO_MODEL_DIR)
        detect_fn = model.signatures['serving_default']
        
        return detect_fn
    
    def load_labels(self):
        """Load the label map"""
        # This would normally load from a file, but for simplicity we'll define common objects
        return {
            1: {'name': 'person'},
            2: {'name': 'bicycle'},
            3: {'name': 'car'},
            4: {'name': 'motorcycle'},
            5: {'name': 'airplane'},
            6: {'name': 'bus'},
            7: {'name': 'train'},
            8: {'name': 'truck'},
            9: {'name': 'boat'},
            # ... more objects would be defined here
        }
    
    def get_frame(self):
        """Capture a frame from the camera"""
        ret, frame = self.camera.read()
        if not ret:
            return None
        return frame
    
    def detect_objects(self, frame):
        """Detect objects in the frame"""
        # Convert to RGB (TensorFlow models expect RGB)
        image_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # The input needs to be a tensor
        input_tensor = tf.convert_to_tensor(image_np)
        # Add batch dimension
        input_tensor = input_tensor[tf.newaxis, ...]
        
        # Run inference
        detections = self.detect_fn(input_tensor)
        
        # Process results
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() 
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        
        return detections
    
    def analyze_scene(self, frame):
        """Analyze the scene and return a description"""
        if frame is None:
            return "I cannot see anything at the moment."
        
        detections = self.detect_objects(frame)
        
        # Filter detections with confidence > 0.5
        indices = np.where(detections['detection_scores'] > 0.5)[0]
        
        if len(indices) == 0:
            return "I don't see any recognizable objects."
        
        # Count objects by class
        objects = {}
        for i in indices:
            class_id = detections['detection_classes'][i]
            if class_id in self.category_index:
                obj_name = self.category_index[class_id]['name']
                if obj_name in objects:
                    objects[obj_name] += 1
                else:
                    objects[obj_name] = 1
        
        # Create description
        description = "I can see "
        object_phrases = []
        for obj_name, count in objects.items():
            if count == 1:
                object_phrases.append(f"a {obj_name}")
            else:
                object_phrases.append(f"{count} {obj_name}s")
        
        if len(object_phrases) == 1:
            description += object_phrases[0]
        elif len(object_phrases) == 2:
            description += f"{object_phrases[0]} and {object_phrases[1]}"
        else:
            description += ", ".join(object_phrases[:-1]) + f", and {object_phrases[-1]}"
        
        return description
    
    def detect_text(self, frame):
        """Detect and read text in the image"""
        # This would use OCR (e.g., Tesseract)
        # For simplicity, we'll return a placeholder
        return "No text detected"
    
    def __del__(self):
        """Clean up resources"""
        self.camera.release()
