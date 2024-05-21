import speech_recognition as sr
import win32com.client
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
from box import ConfigBox 
import json
import requests

class Utils:
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
        
    def run_program(self,command):
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

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio,language='en-in')
                print(f'user said {query}')
                return query
            except Exception as e:
                return "Sorry, I could'nt catch what you were saying."

def read_json(file_path)->ConfigBox:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return ConfigBox(data)


def get_spotify_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    # Send the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content (JSON data)
        return response.json()["access_token"]
    else:
        # Print an error message if the request was not successful
        print("Error:", response.status_code)

