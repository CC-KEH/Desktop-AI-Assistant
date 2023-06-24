import speech_recognition as sr
import win32com.client
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess


class assistant:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        # Get the list of available voices
        voices = self.speaker.GetVoices()  
        # Loop through the voices to find the Catherine voice
        for voice in voices:
            if voice.GetDescription() == 'Microsoft Catherine':
                # Set the voice as the active voice
                self.speaker.Voice = voice
                break
            
    
    def say(self,text):
        self.speaker.speak(f"{text}") 
        
    def open_program(self,command):
        try:
            # Execute a system command to find the program path
            result = subprocess.run(['where', command], capture_output=True, text=True)
            output = result.stdout.strip()

            if output:
                program_path = output.split('\n')[0]
                self.say(f'opening {command}')
                subprocess.Popen(program_path)
                print(f"Opened {command} successfully!")
            else:
                print(f"Program '{command}' not found.")
        except OSError as e:
            print(f"Error opening {command}: {e}")

    def take_command():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio,language='en-in')
                print(f'user said {query}')
                return query
            except Exception as e:
                return "Sorry, I could'nt catch what you were saying."