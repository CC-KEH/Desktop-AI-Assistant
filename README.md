# Requirements:

## Python 3.11.2
# Setup
## After cloning run the following commands:
    pip install speechrecognition   
    pip install wikipedia
    pip install openai
    pip install spotipy
    install pyAudio:
        1. Pycharm - just install from packages
        2. VSCODE or other editor - goto "https://www.lfd.uci.edu/~gohlke/pythonlibs/" click on pyaudio, download for your python version, put the downloaded whl file in project folder and run "pip install 'file name' " 
    For WINDOWS -> python -m pip install --upgrade pywin32 
    For MacOs -> no need

## Spotify Setup
### Create a spotify [developer account](https://developer.spotify.com/)
### Goto Dashboard, create App, fill details, ignore Website box, write http://localhost/4000 in RedirectURL.
### After creating app Get client id, client secret and replace it with the clientID, clientSecret in main.py
### You are good to go.



    