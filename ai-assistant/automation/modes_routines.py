import json
import random
import webbrowser
from tools.utils import *
from saved_data.constants import *
from connections.player import SpotipyPlayer
from connections.google import Google
from connections.notion import Notion

class Mode:
    def __init__(self):
        self.modes = ['work', 'study', 'sleep','play']
        self.utils = Utils()    
        self.player = SpotipyPlayer()

    def run_program(self, query, third_party=False):
        if not third_party:
            self.utils.run_program(query)
        else:
            if query in applications.keys():
                subprocess.run(['powershell', '-Command', applications[query]])
            elif query in games.keys():
                subprocess.run(['powershell', '-Command', games[query]])
            else:
                self.speak("I cant find the program.")
    
    def work_mode(self):
        todos = self.notion.get_data('todos')
        self.utils.speak("Today's schedule is as follows")
        for todo in todos:
            self.utils.speak(todo['task'])
        # Open VSCODE
        self.run_program('code')
        # Play Spotify, 100X Devloper Playlist
        self.player.controller(session_type='playlist', session=random.choice(playlists['work']),task='play')
    
    def study_mode(self):
        # study mode functionalities
        # Open obsidian
        self.run_program('Obsidian', third_party=True)
        # Open site
        webbrowser.open(study_utils['site'])
        # Play Spotify, Study Playlist
        self.player.controller(session_type='playlist', session=random.choice(playlists['work']),task='play')
            
    def game_mode(self):
        # play mode functionalities
        # Open Genshin Impact or Open Steam or Open Valorant
        program = random.choice(list(games.keys()))
        self.run_program(program, third_party=True)
        # Play Spotify if opened Genshin Impact or Valorant
        self.player.controller(session_type='playlist', session=random.choice(playlists['play']),task='play')
            
    def sleep_mode(self):
        # sleep mode functionalities
        # Turn of Spotify if playing
        self.player.controller(session_type='playlist', session=random.choice(playlists['play']),task='pause')
        # Play YT ASMR Playlist
        webbrowser.open(f"{random.choice(asmr_playlists.values())}")
        # turn brightness to 0
        control_brightness(0,0)
        
    
class Routine:
    def __init__(self):
        self.utils = Utils()
        self.google = Google()
        self.notion = Notion()

    def morning(self):
        # Get mails
        mails = self.google.get_mails()
        self.speak("You have " + str(len(mails)) + " new mails.")
        for mail in mails:
            self.speak("Subject: ",mail['subject'])
        # Get Todos
        self.speak("Today's schedule is as follows")
        todos = self.notion.get_data('todos')
        for todo in todos:
            self.speak(todo['task'])

    def night(self):
        # Summary of the day
        with open('saved_data/summary.json', 'r') as f:
            summary = json.load(f)
        last_date = list(summary.keys())[-1]
        self.speak("Here's what you did today,",summary[last_date])
        # Open Notion
        self.run_program('Notion', third_party=True)
        # Open Camera for Video Jounal
        os.system("start microsoft.windows.camera:")
        # Close the program
        run = False