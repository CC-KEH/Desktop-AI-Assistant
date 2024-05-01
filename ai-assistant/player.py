import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from dotenv import load_dotenv
import requests
from config import access_token
load_dotenv()

class Player:
    def __init__(self):
        self.clientID = '<ClientID>'
        self.clientSecret = '<ClientSecretID>'
        self.redirect_url = 'http://localhost/4000'
        self.tasks = ['play', 'pause', 'next', 'previous', 'seek', 'repeat', 'shuffle']
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.clientID, client_secret=self.clientSecret))

    def send_request(self,task: str) -> None:
        if task not in self.tasks:
            raise ValueError('Invalid Task')
        spotify_url = f"https://api.spotify.com/v1/me/player/{task}"
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json',
        }
        data = {
            "context_uri": "spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
            "offset": {
                "position": 5
            },
            "position_ms": 0
        }
        response = requests.put(spotify_url, headers=headers, json=data)

    def controller(self,task):
        if task not in self.tasks:
            raise ValueError('Invalid Task')
        else:
            self.send_request(task)