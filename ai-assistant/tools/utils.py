import screen_brightness_control as sbc
import speech_recognition as sr
import win32com.client
import subprocess
from box import ConfigBox 
import json
import requests
from fuzzywuzzy import fuzz
import spacy 
import os

nlp = spacy.load("en_core_web_sm")
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
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Error:", response.status_code)



def find_best_match(self, query, items):
    best_match = None
    highest_score = 0
    for item in items:
        name = item['name']
        score = fuzz.ratio(query.lower(), name.lower())
        if score > highest_score:
            highest_score = score
            best_match = item
    return best_match, highest_score

def extract_entities(sentence):
    doc = nlp(sentence)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities


def search_file(directory, filename):
    for dirpath, dirnames, files in os.walk(directory):
        if filename in files:
            return os.path.join(dirpath, filename)
    return None




def control_brightness(level=100, display=0):
    # get the brightness
    brightness = sbc.get_brightness()
    # get the brightness for the primary monitor
    primary = sbc.get_brightness(display=0)

    # set the brightness to 100%
    # sbc.set_brightness(100)
    sbc.set_brightness(level, display=0)
    
    # set the brightness to 100% for the primary monitor
    # sbc.get_brightness(100, display=0)

    # show the current brightness for each detected monitor
    # for monitor in sbc.list_monitors():
        # print(monitor, ':', sbc.get_brightness(display=monitor), '%')

