from random import random
import time
import speech_recognition as sr
import webbrowser
import datetime
from utils import *
from organise import Organiser
from brain import *
from automation import Automation
from player import Player
from personality import Personality
from constants import *
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

    def organise(self, query=None):
        # documents in programs in c drive
        # documents \\ programs \\ c drive
        # cdrive \\ programs \\ documents
        with open('organised.txt','r') as file:
            last_organised = file.readlines()
            if len(last_organised) > 0:
                last_organised = last_organised[-1]
                last_organised = last_organised.replace('\n','')
                last_organised = datetime.datetime.strptime(last_organised, '%Y-%m-%d %H:%M:%S.%f')
                
                if (datetime.datetime.now() - last_organised).days < 7:
                    if query!= None:
                        self.speak("I have already organised the files this week. Do you want to organise again?")
                        response = self.take_command()
                        if response.lower() == 'no':
                            return
        if query is None:
            os.chdir('files')
            pwd = os.cwd()
            self.organiser.organise(pwd)
            os.chdir('..')
        else:              
            query = query.title().replace("In", "\\")
            path = list(query.split(" \\ "))
            base_path = "C:\\Users\\assistant_workstation"
            if not os.path.exists(base_path):
                self.speak(random.choice(self.personality["errors"]['no_path']))
            else:
                path.append(base_path)
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
            'last_message_sent': message,
            'time': time.time(),
        }

        with open('whatsapp_data.json', 'w') as f:
            json.dump(data, f)

if __name__ == "__main__":
    assistant = Assistant()

    brain = Brain()
    start_time = time.time()
    news_time = time.time()
    while True:
        print("Listening...")
        if (time.time() - news_time) > (3600*2):
            if "Sports" in random.choice(["Sports", "Tech"]):
                news = assistant.automator.get_sports_news()
                assistant.speak("Here are some sports news")
                for i in news:
                    assistant.speak(i)

            else:
                news = assistant.automator.get_tech_news()
                assistant.speak("Here are some tech news")
                for i in news:
                    assistant.speak(i)
            news_time = time.time()

        if (time.time() - start_time) > (3600*5):
            assistant.speak(random.choice(assistant.personality['sleep']['sleepy']))
            break
                
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
        
        for word in query:
            if word in controls:
                assistant.player.controller(word)
        
        if "search" in query:
            assistant.automator.search(query)
        
        if "message" in query:
            assistant.send_message()
        
        if "exit" in query:
            break
        
        else:
            assistant.speak(random.choice(assistant.personality['dialogs']['misunderstand']))
            continue
