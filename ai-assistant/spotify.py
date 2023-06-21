import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials



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
