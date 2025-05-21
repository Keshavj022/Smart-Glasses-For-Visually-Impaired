import requests
import json
import time
import threading

class GPSNavigator:
    def __init__(self, config):
        self.config = config
        self.current_location = None
        self.home_location = config.get('home_location', None)
        self.api_key = config.get('google_maps_api_key', '')
        
        # Start GPS monitoring thread
        self.gps_thread = threading.Thread(target=self.monitor_gps)
        self.gps_thread.daemon = True
        self.gps_thread.start()
    
    def monitor_gps(self):
        """Monitor GPS data from Arduino"""
        # In a real implementation, this would read GPS data from Arduino
        # For simplicity, we'll simulate GPS data
        while True:
            # Simulated GPS coordinates (would come from Arduino)
            self.current_location = {
                'latitude': 37.7749,
                'longitude': -122.4194
            }
            time.sleep(5)  # Update every 5 seconds
    
    def report_location(self, tts):
        """Report the current location to the user"""
        if not self.current_location:
            tts.speak("I'm sorry, I can't determine your location right now.")
            return
        
        # Reverse geocode to get address
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={self.current_location['latitude']},{self.current_location['longitude']}&key={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'OK':
                address = data['results'][0]['formatted_address']
                tts.speak(f"You are currently at {address}")
            else:
                tts.speak(f"You are at latitude {self.current_location['latitude']} and longitude {self.current_location['longitude']}")
        except Exception as e:
            tts.speak(f"You are at latitude {self.current_location['latitude']} and longitude {self.current_location['longitude']}")
    
    def find_nearby_places(self, place_type, tts):
        """Find nearby places of a specific type"""
        if not self.current_location:
            tts.speak("I'm sorry, I can't determine your location right now.")
            return
        
        try:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={self.current_location['latitude']},{self.current_location['longitude']}&radius=500&type={place_type}&key={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'OK':
                places = data['results'][:3]  # Limit to top 3 results
                
                if not places:
                    tts.speak(f"I couldn't find any {place_type}s nearby.")
                    return
                
                tts.speak(f"I found {len(places)} {place_type}s nearby:")
                for i, place in enumerate(places):
                    distance = self.calculate_distance(
                        self.current_location['latitude'], 
                        self.current_location['longitude'],
                        place['geometry']['location']['lat'],
                        place['geometry']['location']['lng']
                    )
                    tts.speak(f"{i+1}. {place['name']}, approximately {int(distance)} meters away.")
            else:
                tts.speak(f"I couldn't find any {place_type}s nearby.")
        except Exception as e:
            tts.speak(f"I'm sorry, I encountered an error while searching for nearby {place_type}s.")
    
    def navigate_to(self, destination, tts):
        """Provide navigation instructions to a destination"""
        if not self.current_location:
            tts.speak("I'm sorry, I can't determine your location right now.")
            return
        
        # This would use Google Directions API to get navigation instructions
        # For simplicity, we'll provide a placeholder response
        tts.speak(f"Starting navigation to {destination}. Please proceed straight ahead for 100 meters.")
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points in meters (Haversine formula)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Earth radius in meters
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance
