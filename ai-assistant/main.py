import speech_recognition as sr
import os
import win32com.client
speaker = win32com.client.Dispatch('SAPI.SpVoice')

def say(text):
    speaker.speak(f"{text}") 

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio,language='en-in')
            print(f'user said {query}')
            return query
        except Exception as e:
            return "Sorry, I could'nt catch what you were saying."
            
            
if __name__ =="__main__":
    while True:
        print('Listening...')
        text = take_command()
        say(text)