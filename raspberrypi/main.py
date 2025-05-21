#!/usr/bin/env python3
import os
import time
import threading
import json
import serial
from datetime import datetime

# Import custom modules
from camera_processor import CameraProcessor
from text_to_speech import TextToSpeech
from face_recognition import FaceRecognizer
from gps_navigator import GPSNavigator
from setup_wizard import SetupWizard
from emergency_system import EmergencySystem

class SmartGlasses:
    def __init__(self):
        # Initialize configuration
        self.config = self.load_config()
        
        # Check if setup is needed
        if not os.path.exists('config.json') or self.config.get('setup_complete', False) == False:
            self.setup()
        
        # Initialize serial connection to Arduino
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            time.sleep(2)  # Allow time for connection to establish
        except:
            print("Failed to connect to Arduino. Check connection and try again.")
            self.arduino = None
        
        # Initialize modules
        self.tts = TextToSpeech()
        self.camera = CameraProcessor()
        self.face_recognizer = FaceRecognizer(self.config)
        self.gps = GPSNavigator(self.config)
        self.emergency = EmergencySystem(self.config)
        
        # Welcome message
        self.tts.speak(f"Hello {self.config['user_name']}, your smart glasses are ready.")
        
    def load_config(self):
        """Load configuration from file or return default"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {"setup_complete": False}
    
    def setup(self):
        """Run the setup wizard if not already configured"""
        setup = SetupWizard()
        self.config = setup.run_setup()
        with open('config.json', 'w') as f:
            json.dump(self.config, f)
    
    def process_arduino_data(self):
        """Process data received from Arduino"""
        while True:
            if self.arduino:
                try:
                    if self.arduino.in_waiting > 0:
                        data = self.arduino.readline().decode('utf-8').rstrip()
                        if data.startswith("OBSTACLE:"):
                            parts = data.split(":")
                            if len(parts) >= 3:
                                distance = float(parts[1])
                                direction = parts[2]
                                
                                # Alert only for dangerous obstacles (less than 20cm)
                                if distance < 20:
                                    message = f"Warning! Obstacle {direction} at {distance} centimeters."
                                    self.tts.speak(message)
                                    
                        elif data.startswith("GPS:"):
                            # Process GPS data if needed
                            pass
                except Exception as e:
                    print(f"Error reading from Arduino: {e}")
            time.sleep(0.1)
    
    def process_camera(self):
        """Process camera input continuously"""
        while True:
            # Capture and process frame
            frame = self.camera.get_frame()
            
            # Perform face recognition
            faces = self.face_recognizer.identify_faces(frame)
            for face in faces:
                if face['name'] == 'Unknown' and face['confidence'] > 0.7:
                    # Potential new person to add
                    self.tts.speak("I see someone new. Would you like to introduce them?")
                    # Here would be voice command processing to get response
                    # For simplicity, we'll skip this part
            
            # Process for obstacles or scene understanding only when requested
            # to avoid overwhelming the user with information
            
            time.sleep(0.2)  # Reduce processing load
    
    def listen_for_commands(self):
        """Listen for voice commands"""
        # In a real implementation, this would use a speech recognition library
        # For simplicity, we'll simulate with keyboard input
        while True:
            command = input("Enter command (or 'q' to quit): ")
            
            if command.lower() == 'q':
                self.shutdown()
                break
            elif "surrounding" in command.lower():
                self.describe_surroundings()
            elif "where am i" in command.lower():
                self.gps.report_location(self.tts)
            elif "navigate" in command.lower():
                destination = command.lower().replace("navigate to ", "")
                self.gps.navigate_to(destination, self.tts)
            elif "help" in command.lower():
                self.emergency.send_emergency_alert("User requested help")
    
    def describe_surroundings(self):
        """Describe the current surroundings to the user"""
        frame = self.camera.get_frame()
        scene_description = self.camera.analyze_scene(frame)
        self.tts.speak(scene_description)
    
    def shutdown(self):
        """Clean shutdown of the system"""
        self.tts.speak("Shutting down smart glasses. Goodbye.")
        if self.arduino:
            self.arduino.close()
        # Additional cleanup as needed
    
    def run(self):
        """Run the main program loops"""
        # Start threads for different processes
        arduino_thread = threading.Thread(target=self.process_arduino_data)
        arduino_thread.daemon = True
        arduino_thread.start()
        
        camera_thread = threading.Thread(target=self.process_camera)
        camera_thread.daemon = True
        camera_thread.start()
        
        # Main thread handles voice commands
        self.listen_for_commands()

if __name__ == "__main__":
    glasses = SmartGlasses()
    glasses.run()
