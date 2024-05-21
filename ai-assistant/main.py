import random
import time
import webbrowser
import datetime
from utils import *
from organise import Organiser
# from brain import *
from automation import Automation
from player import Player
from constants import *
from personality.chat import *
from personality.personality import Personality
import os
import json
from config import *

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
            self.organiser.organise(pwd,query)
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
                self.organiser.organise(path,query)
    
    def send_message(self, recipient_name, contacts, save_contact):
            recipient_no = contacts.get(recipient_name)
            if recipient_no is None:
                self.speak("Recipient not found.")
                return

            if save_contact:
                contacts[recipient_name] = recipient_no
                with open('contacts.json', 'w') as f:
                    json.dump(contacts, f)

            self.speak("What message do you want to send?")
            message = self.utils.take_command()
            self.speak("What time do you want to send the message?")
            time = self.utils.take_command()

            if "now" in time:
                time = datetime.datetime.now()

            self.speak("Okay, I will send message to " + recipient_name + " at " + str(time))
            self.automator.send_message(phone_no=recipient_no, time=time, message=message, code='+91')
    
    def take_message(self, recipient_name=None):
        self.speak("Who do you want to send a message to?")
        recipient_name = self.utils.take_command().lower()
        try:
            with open('contacts.json', 'r') as f:
                contacts = json.load(f)
        except FileNotFoundError:
            contacts = {}
        
        self.send_message(recipient_name, contacts, recipient_name not in contacts)
        
if __name__ == "__main__":
    assistant = Assistant()

    # brain = Brain()
    start_time = time.time()
    news_time = time.time()
    while True:
        print("Listening...")
        if (time.time() - news_time) > (3600*2):
            topic = random.choice(news_interests)
            news = assistant.automator.get_news(topic=topic)
            assistant.speak(f"Here are some recent news related to {topic}")
            for src,title in news.items():
                assistant.speak(title + " source " + src)
            news_time = time.time()

        if (time.time() - start_time) > (3600*5):
            assistant.speak(random.choice(assistant.personality['dialogs']['sleep']))
            break
                
        query = assistant.utils.take_command()
        model_response = get_response(query)
        
        if ' ' in model_response:
            assistant.speak(model_response)
            continue
        else:
            try:
                task = model_response[0]
                entity = model_response[1]
            except IndexError:
                entity = None
                
            if task == 'organise':
                assistant.organise(entity)
                
            elif task == 'ask_gpt':
                if entity is None:
                    assistant.speak("What was your question about?")
                    entity = assistant.utils.take_command()
                # assistant.speak(brain.ask(question=entity))

            elif task == "open_site":
                for site in sites:
                    if f"Open {site[0]}".lower() in query.lower():
                        assistant.speak(f"opening {site[0]}")
                        webbrowser.open(f"{site[1]}")
                
            elif task == 'send_message':
                if entity is None:
                    assistant.take_message()
                else:
                    assistant.take_message(entity)
                    
            elif task == 'search':
                assistant.automator.search(entity)
                
            elif task == 'run_program':
                assistant.run_program(entity)
                
            elif task == 'play_music':
                assistant.player.controller(entity)
            
            elif task == "control_player":
                for word in controls:
                    if word in query:
                        assistant.player.controller(word)
                
            elif task == 'news':
                if entity is None:
                    entity = random.choice(news_interests)
                news = assistant.automator.get_news(topic=entity)
                assistant.speak(f"Here are some recent news related to {entity}")
                for src,title in news.items():
                    assistant.speak(title + " source " + src)
            
            elif task == 'summarize':
                # entity will be a path to a file
                assistant.automator.summarize(entity)
            
            elif task == 'suggestions':
                assistant.automator.suggestions(entity)
            
            elif task == 'bored':
                # assistant.speak(brain.ask(question="I am bored"))
                # Open fav sites or play music or suggest something or yt video
                pass
            
            elif task == 'get_weather':
                assistant.automator.get_weather(entity)
            
            elif task == 'exit':
                break
            
            else:
                assistant.speak(random.choice(assistant.personality['dialogs']['misunderstand']))
                print("I dont understand")
                continue        
        
        
        
        # for site in sites:
        #     if f"Open {site[0]}".lower() in query.lower():
        #         assistant.speak(f"opening {site[0]}")
        #         webbrowser.open(f"{site[1]}")
        
        # for word in controls:
        #     if word in query:
        #         assistant.player.controller(word)
                
        # if "open" in query:
        #     command = query.lower().replace("open ", "")
        #     assistant.run_program(command)

        # if "organise" in query:
        #     assistant.organise(query)

        # if any(query.startswith(word) for word in question_identifier):
        #     # assistant.speak(brain.ask(question=query))
        #     print("I dont have a brain yet")
        
        # if "search" in query:
        #     assistant.automator.search(query)
        
        # if "message" in query:
        #     assistant.send_message()
        
        # if "exit" in query:
        #     break
        
        # else:
        #     assistant.speak(random.choice(assistant.personality['dialogs']['misunderstand']))
        #     print("I dont understand that command")
        #     continue
