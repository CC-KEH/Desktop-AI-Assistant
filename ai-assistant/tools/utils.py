import screen_brightness_control as sbc
import speech_recognition as sr
import win32com.client
import subprocess
from box import ConfigBox 
import json
from fuzzywuzzy import fuzz
import spacy 
import os

from saved_data.constants import applications, games

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
    
    def run_program(self, query, third_party=False):
        if not third_party:
            try:
                # Execute a system command to find the program path
                result = subprocess.run(['where', query], capture_output=True, text=True)
                output = result.stdout.strip()

                if output:
                    program_path = output.split('\n')[0]
                    self.say(f'opening {query}')
                    subprocess.Popen(program_path)
                    print(f"Opened {query} successfully!")
                else:
                    print(f"Program '{query}' not found.")

            except OSError as e:
                print(f"Error opening {query}: {e}")
            
        else:
            if query in applications.keys():
                subprocess.run(['powershell', '-Command', applications[query]])
            elif query in games.keys():
                subprocess.run(['powershell', '-Command', games[query]])
            else:
                self.say("I cant find the program.")
    

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


def find_best_match(query, items):
    best_match = None
    highest_score = 0
    for item in items:
        name = item['name']
        score = fuzz.ratio(query.lower(), name.lower())
        if score > highest_score:
            highest_score = score
            best_match = item
    return best_match, highest_score

def search_file(directory, filename):
    for dirpath, dirnames, files in os.walk(directory):
        if filename in files:
            return os.path.join(dirpath, filename)
    return None


def control_brightness(level=100, display=0):
    # brightness = sbc.get_brightness()
    # primary = sbc.get_brightness(display=display)
    sbc.set_brightness(level, display=display)