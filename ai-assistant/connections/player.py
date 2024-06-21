import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
clientID = os.getenv("spotify_clientID")
clientSecret = os.getenv("spotify_clientSecret")
user_id = os.getenv("spotify_user_id")
redirect_uri = os.getenv("spotify_redirect_uri")

class SpotipyPlayer:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirect_uri, scope="user-read-playback-state,user-modify-playback-state,playlist-read-private"))

    def play(self, uri):
        self.sp.start_playback(uris=[uri])

    def pause(self):
        self.sp.pause_playback()

    def next(self):
        self.sp.next_track()

    def previous(self):
        self.sp.previous_track()

    def search(self, query):
        result = self.sp.search(q=query, limit=1)
        return result['tracks']['items'][0]['uri']

    def get_current_track(self):
        return self.sp.current_playback()

    def get_playlists(self):
        return self.sp.current_user_playlists()

    def format_playlists(self, playlists):
        return [(playlist['name'],playlist['id']) for playlist in playlists['items']]

    def get_playlist_tracks(self, playlist_id):
        return self.sp.playlist_tracks(playlist_id)

    def get_playlist_id(self, playlist_name):
        playlists = self.get_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                return playlist['id']
        return None

    def play_playlist(self, playlist_name=None, playlist_id=None):
        if playlist_id is None:
            playlist_id = self.get_playlist_id(playlist_name)
        tracks = self.get_playlist_tracks(playlist_id)
        uris = [track['track']['uri'] for track in tracks['items']]
        self.sp.start_playback(uris=uris)

    def play_playlist_track(self, playlist_name, track_number):
        playlist_id = self.get_playlist_id(playlist_name)
        tracks = self.get_playlist_tracks(playlist_id)
        uri = tracks['items'][track_number]['track']['uri']
        self.sp.start_playback(uris=[uri])
    
    def play_random_playlist(self):
        playlists = self.get_playlists()
        playlist = playlists['items'][int(random() * len(playlists['items']))]
        playlist_id = playlist['id']
        tracks = self.get_playlist_tracks(playlist_id)
        uris = [track['track']['uri'] for track in tracks['items']]
        self.sp.start_playback(uris=uris)
    
    
if __name__ == "__main__":
    player = SpotipyPlayer()
    query = "play some song"
    if 'some' or 'something' in query:
        playlists = player.get_playlists()
        print(playlists)
        playlists = player.format_playlists(playlists)
        print(playlists)
        player.play_playlist(random.choice(playlists)[0])
        # player.play_playlist(playlist)
    else:
        if 'play' in query:
            query = query.replace('play','')
        if 'song' in query:
            query = query.replace('song','')
        song_name = query
        song = player.search(song_name)
        print(song)
        player.play(song)
