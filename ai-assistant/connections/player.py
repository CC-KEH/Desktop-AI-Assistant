from random import random
import requests
from config import *
from utils import get_spotify_token, find_best_match

class Player:
    def __init__(self):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.redirect_url = 'http://localhost/4000'
        self.tasks = ['play', 'pause', 'next', 'previous', 'seek', 'repeat', 'shuffle', 'currently-playing']
        self.token = get_spotify_token(self.clientID, self.clientSecret)
        self.header = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }

    def start_playback(self, task: str, session_type='', session='') -> None:
        
        print(f"Will send the {task} request to Spotify API")
        
        if session_type == 'playlist':
            session_id = session['id']
            playlist_context_uri = f"spotify:playlist:{session_id}"
            data = {
            # "context_uri": playlist_context_uri,
            "position_ms": 0
            }

        else:
            data = {
            "position_ms": 0
            }
        
        spotify_url = f"https://api.spotify.com/v1/me/player/{task}"

        headers = self.header
        
        response = requests.put(spotify_url, headers=headers, json=data)

    def send_request(self,task):
        data = {"position_ms": 0}
        spotify_url = f"https://api.spotify.com/v1/me/player/{task}"
        response = requests.put(spotify_url, headers=self.header, json=data)
    
    def get_playlists(self):
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        data = {
            "limit": 10,
            "offset": 0
        }
        response = requests.put(url, headers=self.header,json=data)
        playlists = []
    
        for playlist in response['items']:
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            playlist_data = {
                "id": playlist_id,
                "name": playlist_name
            }
            playlists.append(playlist_data)

        return playlists
    
    def play_random(self):
        spotify_url = f"https://api.spotify.com/v1/me/player/play"
        playlists = self.get_playlists()
        playlist_ids = [playlist['id'] for playlist in playlists]
        playlist_context_uri = random.choice(playlist_ids)
        data = {
            "context_uri": playlist_context_uri,
            "position_ms": 0
        }
        response = requests.put(spotify_url, headers=self.headers, json=data)
    
    def controller(self,session_type,session,task):
        if task not in self.tasks:
            raise ValueError('Invalid Task')
        
        elif task == 'play' or task == 'resume':
            self.start_playback(task, session_type, session)
            
        else:
            self.send_request(task)

if __name__ == "__main__":
    player = Player()
    playlists = player.get_playlists()
    session_type = 'playlist'
    player.controller(session_type,playlists[0],'play')
    