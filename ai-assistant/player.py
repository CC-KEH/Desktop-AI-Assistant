from email import utils
from random import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from dotenv import load_dotenv
import requests
from config import *
from utils import get_spotify_token
load_dotenv()

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
        
    def send_request(self,task: str) -> None:
        
        print(f"Will send the {task} request to Spotify API")
        
        album_id = '5ht7ItJgpBH7W6vJ5BqpPr'
        
        spotify_url = f"https://api.spotify.com/v1/me/player/{task}"
        
        album_context_uri = f"spotify:album:{album_id}"
        
        playlist_context_uri = random.choice(self.get_playlists())

        headers = self.header
        
        data = {
            "context_uri": album_context_uri,
            # "offset": {
            #     "position": 5
            # },
            "position_ms": 0
        }
        
        response = requests.put(spotify_url, headers=headers, json=data)

    def get_playlists(self):
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        data = {
            "limit": 10,
            "offset": 0
        }
        response = requests.put(url, headers=self.header,json=data)
        playlists_uris = []
    
        for playlist in response['items']:
            playlists_uris.append(playlist['uri'])
    
        return playlists_uris
    
    def recommentations(self):
        url = f"https://api.spotify.com/v1/recommendations"
        
        data = {
            "limit": 10,
            "seed_artists": "4NHQUGzhtTLFvgF5SZesLK",
            "seed_genres": "techno,trance,dance,electronic,house",
            "seed_tracks": "0c6xIDDpzE81m2q797ordA"
        }
        
        response = requests.put(url, headers=self.header,json=data)
        
    
    def controller(self,task):
        if task not in self.tasks:
            raise ValueError('Invalid Task')
        else:
            self.send_request(task)