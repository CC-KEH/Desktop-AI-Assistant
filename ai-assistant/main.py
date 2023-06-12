import speech_recognition as sr
import os
import win32com.client
import webbrowser
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
speaker = win32com.client.Dispatch('SAPI.SpVoice')


clientID = '<ClientID>'
clientSecret = '<ClientSecretID>'
redirect_uri = 'http://localhost/4000'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID,client_secret=clientSecret))

while True:
    print("Welcome, C.C")
    print("0 - Exit")
    print("1 - Search for a Song")
    choice = int(input("Your Choice: "))
    if choice == 1:
        searchQuery = input("Enter Song Name: ")
        searchResults = sp.search(searchQuery,1,0,"track")
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        webbrowser.open(song)
        print('Song has opened in your browser.')
    elif choice == 0:
        break
    else:
        print("Enter valid choice.")

def say(text):
    speaker.speak(f"{text}") 

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio,language='en-in')
            print(f'user said {query}')
            return query
        except Exception as e:
            return "Sorry, I could'nt catch what you were saying."
            
            
if __name__ =="__main__":
    sites = [['youtube','https://youtube.com'],['google','https://google.com'],['twitch','https://twitch.tv'],['wikipedia','https://wikipedia.com']]
    while True:
        print('Listening...')
        query = take_command()
        for site in sites:
            if(f"Open {site[0]}".lower() in query.lower()):
                say(f"opening {site[0]}")
                webbrowser.open(f'{site[1]}')
        if('open music' in query):
            musicPath = '<Path>'
            os.startfile(musicPath)
            