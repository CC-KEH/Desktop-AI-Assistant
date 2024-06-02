from random import random
import requests
from credentials.credentials import clientID, clientSecret, user_id, redirect_uri
from tools.utils import get_access_token, get_spotify_token
import json

class Player:
    def __init__(self):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.user_id = user_id
        self.redirect_uri = redirect_uri
        self.tasks = ['play', 'pause', 'next', 'previous', 'seek', 'repeat', 'shuffle', 'currently-playing']
        self.scope = 'user-modify-playback-state user-read-playback-state playlist-read-private'
        self.token = get_spotify_token(self.clientID, self.clientSecret)
        self.access_token = get_access_token(self.scope, self.clientID, self.clientSecret, self.redirect_uri)['access_token']
        self.access_header = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        self.header = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def start_playback(self, task: str, session_type='', session='') -> None:
        print(f"Will send the {task} request to Spotify API")
        
        data = {"position_ms": 0}
        
        if session_type == 'playlist':
            session_id = session['id']
            playlist_context_uri = f"spotify:playlist:{session_id}"
            data["context_uri"] = playlist_context_uri
        
        spotify_url = f"https://api.spotify.com/v1/me/player/{task}"
        response = requests.put(spotify_url, headers=self.access_header, json=data)
        
        if response.status_code != 204:
            print(f"Error: {response.status_code} - {response.json()}")

    def send_request(self, task):
        data = {"position_ms": 0}
        spotify_url = f"https://api.spotify.com/v1/me/player/{task}"
        response = requests.put(spotify_url, headers=self.access_header, json=data)
        
        if response.status_code != 204:
            print(f"Error: {response.status_code} - {response.json()}")

    def get_playlists(self):
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        params = {
            "limit": 10,
            "offset": 0
        }
        response = requests.get(url, headers=self.header, params=params)
        
        print(json.dumps(response.json(), indent=4))  
        
        if response.status_code == 200:
            playlists = []
            
            for playlist in response.json()['items']:
                playlist_id = playlist['id']
                playlist_name = playlist['name']
                playlist_data = {
                    "id": playlist_id,
                    "name": playlist_name
                }
                playlists.append(playlist_data)
            return playlists
        else:
            print(f"Error: {response.status_code} - {response.json()}")
            return []

    def play_random(self):
        spotify_url = f"https://api.spotify.com/v1/me/player/play"
        playlists = self.get_playlists()
        if playlists:
            playlist_ids = [playlist['id'] for playlist in playlists]
            playlist_context_uri = f"spotify:playlist:{random.choice(playlist_ids)}"
            data = {
                "context_uri": playlist_context_uri,
                "position_ms": 0
            }
            response = requests.put(spotify_url, headers=self.header, json=data)
            
            if response.status_code != 204:
                print(f"Error: {response.status_code} - {response.json()}")
        else:
            print("No playlists available to play.")

    def controller(self, session_type='playlist', session='6cgA8p53Q5Sc383KMmjRbT', task='play'):
        if task not in self.tasks:
            raise ValueError('Invalid Task')
        elif task == 'play' or task == 'resume':
            self.start_playback(task, session_type, session)
        else:
            self.send_request(task)


if __name__ == "__main__":
    player = Player()
    playlists = player.get_playlists()
    player.controller(task='pause')

    if playlists:
        session_type = 'playlist'
        player.controller(session_type, playlists[0], 'play')
    else:
        print("No playlists found.")
