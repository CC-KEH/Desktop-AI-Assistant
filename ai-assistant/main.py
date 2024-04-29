import time
import speech_recognition as sr
import webbrowser
from utils import *
from organise import Organiser
from ai import *
from automation import Automation
from player import Player
from personality import Personality
import os

class Assistant:
    def __init__(self):
        self.personality = Personality()
        self.utils = Utils()
        self.organiser = Organiser()
        self.player = Player()
        self.automator = Automation()
        
    def speak(self, text):
        self.utils.say(text)

    def listen(self):
        self.utils.take_command()

    def run_program(self, query):
        self.utils.run_program(query)

    def organise(self, query):
        # documents in programs in c drive
        # documents \\ programs \\ c drive
        # cdrive \\ programs \\ documents
        query = query.title().replace("In", "\\")
        path = list(query.split(" \\ "))
        path.append("C:\\Users")
        path.pop(0)
        path.reverse()
        self.organiser.organise(path)

    def send_message(self):
        self.speak("Can you tell the Number you want to send a message to?")
        recipient_no = self.take_command()
        self.speak("What is the name of the recipient?")
        recipient_name = self.take_command()
        self.speak("What message do you want to send?")
        message = self.take_command()
        self.speak("What time do you want to send the message?")
        time = self.take_command()
        self.speak("Okay, I will send message to " + recipient_no + " at " + time)
        self.automator.send_message(phone_no=recipient_no,time=time,message=message, code='+91')

        # Save the data
        data = {
            'name': recipient_name,
            'phone_no': recipient_no,
            'last_message_sent': message
        }

        with open('whatsapp_data.json', 'w') as f:
            json.dump(data, f)

if __name__ == "__main__":
    assistant = Assistant()

    brain = Brain()

    sites = [
        ["youtube", "https://youtube.com"],
        ["google", "https://google.com"],
        ["twitch", "https://twitch.tv"],
        ["wikipedia", "https://wikipedia.com"],
    ]
    question_identifier = [
        "what",
        "which",
        "who",
        "when",
        "how",
        "do",
        "does",
        "is",
        "are",
        "can",
        "could",
        "should",
        "would",
        "will",
        "shall",
        "did",
        "was",
        "were",
        "have",
        "has",
        "had",
        "may",
        "am",
    ]
    while True:
        print("Listening...")
        query = assistant.take_command()
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                assistant.speak(f"opening {site[0]}")
                webbrowser.open(f"{site[1]}")

        if "open" in query:
            command = query.lower().replace("open ", "")
            assistant.run_program(command)

        if "organise" in query:
            assistant.organise(query)

        if query.startswith([word for word in question_identifier]):
            assistant.speak(brain.ask(question=query))
        
        if "play" in query:
            assistant.player.play(query)
        
        if "exit" in query:
            break
        
        if "search" in query:
            assistant.automator.search(query)
        
        if "message" in query:
            assistant.send_message()
        
        else:
            assistant.speak("I am not sure what you said. Can you please repeat?")
            continue
