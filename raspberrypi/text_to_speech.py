import pyttsx3
from gtts import gTTS
import os
import tempfile
import pygame

class TextToSpeech:
    def __init__(self, use_offline=True):
        self.use_offline = use_offline
        
        if use_offline:
            # Initialize the offline TTS engine
            self.engine = pyttsx3.init()
            # Set properties
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        else:
            # Initialize pygame for playing audio files (for gTTS)
            pygame.mixer.init()
    
    def speak(self, text):
        """Convert text to speech and play it"""
        if not text:
            return
        
        print(f"Speaking: {text}")
        
        if self.use_offline:
            # Use offline pyttsx3
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            # Use Google's TTS service
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(tmp_file.name)
                
                # Play the audio
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Clean up
                pygame.mixer.music.unload()
                os.unlink(tmp_file.name)
