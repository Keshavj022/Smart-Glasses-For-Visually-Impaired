import json
from text_to_speech import TextToSpeech

class SetupWizard:
    def __init__(self):
        self.tts = TextToSpeech()
        self.config = {}
    
    def run_setup(self):
        """Run the setup wizard to configure the smart glasses"""
        self.tts.speak("Welcome to Smart Glasses setup. I'll ask you a few questions to personalize your experience.")
        
        # Get user name
        self.tts.speak("What is your name?")
        self.config['user_name'] = input("Your name: ")
        
        # Get emergency contact
        self.tts.speak(f"Hello {self.config['user_name']}. Who should I contact in case of emergency?")
        self.config['emergency_contact_name'] = input("Emergency contact name: ")
        
        self.tts.speak("What is their phone number?")
        self.config['emergency_contact_phone'] = input("Emergency contact phone: ")
        
        # Get home location
        self.tts.speak("Is your current location your home?")
        is_home = input("Is this your home? (yes/no): ").lower()
        
        if is_home == 'yes':
            self.tts.speak("I'll remember this as your home location.")
            # In a real implementation, this would get the current GPS coordinates
            self.config['home_location'] = {
                'latitude': 37.7749,
                'longitude': -122.4194,
                'address': "Home"
            }
        else:
            self.tts.speak("Please enter your home address.")
            home_address = input("Home address: ")
            self.config['home_location'] = {
                'address': home_address
                # In a real implementation, this would geocode the address to get coordinates
            }
        
        # Additional settings
        self.tts.speak("Would you like me to speak at a slow, medium, or fast pace?")
        speech_rate = input("Speech rate (slow/medium/fast): ").lower()
        self.config['speech_rate'] = speech_rate
        
        # Complete setup
        self.config['setup_complete'] = True
        self.tts.speak("Setup complete! Your smart glasses are now personalized.")
        
        return self.config
