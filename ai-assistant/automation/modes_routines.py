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
        self.notion = Notion()
        
    def run_program(self, query, third_party=False):
        if not third_party:
            self.utils.run_program(query)
        else:
            if query in applications.keys():
                subprocess.run(['powershell', '-Command', applications[query]])
            elif query in games.keys():
                subprocess.run(['powershell', '-Command', games[query]])
            else:
                self.utils.say("I cant find the program.")
    
    def work_mode(self):
        todos = self.notion.get_data('todos')
        self.utils.say("Today's schedule is as follows")
        for todo in todos:
            self.utils.say(todo['task'])
        # Open VSCODE
        self.run_program('code')
        # Play Spotify, 100X Devloper Playlist
        self.player.play_playlist(playlist_id=random.choice(playlists['work']))
        
    def study_mode(self):
        # study mode functionalities
        # Open obsidian
        self.run_program('obsidian', third_party=True)
        # Open site
        webbrowser.open(study_utils['site'])
        # Play Spotify, Study Playlist
        self.player.play_playlist(playlist_name='study')
            
    def game_mode(self):
        # play mode functionalities
        # Open Genshin Impact or Open Steam or Open Valorant
        program = random.choice(list(games.keys()))
        self.run_program(program, third_party=True)
        # Play Spotify if opened Genshin Impact or Valorant
        self.player.play_playlist(playlist_id=random.choice(playlists['play']))
            
    def sleep_mode(self):
        # sleep mode functionalities
        # Turn of Spotify if playing
        self.player.pause()
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
        print("Morning Routine")
        # Get mails
        mails = self.google.get_mails()
        self.utils.say("You have " + str(len(mails)) + " new mails.")
        self.utils.say("Here are recent 5 mails")
        for mail in mails[:5]:
            self.utils.say(f"Subject: {mail[1]}")
        # Get Todos
        self.utils.say("Today's schedule is as follows")
        todos = self.notion.get_data('todos')
        for todo in todos:
            self.utils.say(todo['task'])

    def night(self):
        print("Night Routine")
        # Summary of the day
        with open('saved_data/summary.json', 'r') as f:
            summary = json.load(f)
        last_date = list(summary.keys())[-1]
        self.utils.say(f"Here's what you did today, {summary[last_date]}")
        # Open Notion
        self.utils.run_program('notion', third_party=True)
        # Open Camera for Video Jounal
        os.system("start microsoft.windows.camera:")