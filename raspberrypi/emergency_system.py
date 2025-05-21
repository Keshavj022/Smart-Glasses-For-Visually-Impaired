import requests
import json
from datetime import datetime

class EmergencySystem:
    def __init__(self, config):
        self.config = config
        self.emergency_contact = config.get('emergency_contact_phone', '')
        self.user_name = config.get('user_name', 'User')
        # API key for SMS service (e.g., Twilio)
        self.api_key = config.get('sms_api_key', '')
    
    def send_emergency_alert(self, threat_details):
        """Send emergency alert with location and threat details"""
        # In a real implementation, this would use the Twilio API or similar service
        # For demonstration purposes, we'll just print the message
        
        # Get current location (would come from GPS)
        location = {
            'latitude': 37.7749,
            'longitude': -122.4194
        }
        
        # Create Google Maps link
        maps_link = f"https://maps.google.com/?q={location['latitude']},{location['longitude']}"
        
        # Format message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"EMERGENCY ALERT: {self.user_name} may need assistance. Threat detected: {threat_details}. Location: {maps_link}. Time: {timestamp}"
        
        print(f"Sending emergency SMS to {self.emergency_contact}: {message}")
        
        # In a real implementation:
        # self.send_sms(self.emergency_contact, message)
        
        return True
    
    def send_sms(self, to_number, message):
        """Send SMS using an API service"""
        # This would use Twilio or similar service
        # Example with Twilio:
        """
        from twilio.rest import Client
        
        client = Client(self.config['twilio_account_sid'], self.config['twilio_auth_token'])
        message = client.messages.create(
            body=message,
            from_=self.config['twilio_phone_number'],
            to=to_number
        )
        """
        pass
