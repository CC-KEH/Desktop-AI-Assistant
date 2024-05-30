import os
import json
import time
import random
import datetime
import webbrowser
from tools.utils import *
from connections.brain import *
from saved_data.config import *
from saved_data.constants import *
from saved_data.contacts import contacts
from connections.notion import Notion
from connections.player import Player
from tools.organise import Organiser
from automation.automation import Automation
from personality.chat import *
from personality.personality import personality

class Assistant:
    def __init__(self):
        self.utils = Utils()
        self.organiser = Organiser()
        self.player = Player()
        self.automator = Automation()
        self.personality = personality
        
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
                self.speak(random.choice(self.personality['dialogs']["errors"]['no_path']))
            else:
                path.append(base_path)
                path.pop(0)
                path.reverse()
                self.organiser.organise(path,query)
    
    def send_message(self, recipient_name, save_contact):
            recipient_no = contacts[recipient_name]
            if recipient_no is None:
                self.speak("Recipient not found.")
                return

            if save_contact:
                contacts.update({recipient_name: recipient_no})

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
        self.send_message(recipient_name, recipient_name not in contacts)
        
if __name__ == "__main__":
    assistant = Assistant()
    assistant_name = 'Makima'
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
        if query.startswith(assistant_name) or query.startswith(f"hey {assistant_name}"):
            
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

                elif task =='notion':
                    if 'notion' in query:
                        query = query.replace('notion','')
                    notion = Notion()
                    if 'movie' in query:
                        movies = notion.get_data(asked_for='movies')
                        movie = random.choice(movies)
                        assistant.speak(f"You can watch {movie['name']}")

                    elif 'book' in query:
                        books = notion.get_data(asked_for='books')
                        book = random.choice(books)
                        assistant.speak(f"You can read {books['name']}")

                    elif 'anime' in query:
                        animes = notion.get_data(asked_for='animes')
                        anime = random.choice(animes)
                        assistant.speak(f"You can watch {animes['name']}")

                    elif 'task' in query:
                        if 'complete' in query:
                            todo = find_best_match('task', query.split(''))
                            if todo is None:
                                assistant.speak("I could not find the task you are talking about")
                            else:
                                todos = notion.get_data(asked_for='todos')
                                for t in todos:
                                    if t['task'] == todo:
                                        todo = t
                                        break
                                notion.update_item(item=todo, asked_for='todos')
                                assistant.speak(f"Marked {todo['task']} as complete")
                        else:
                            todos = notion.get_data(asked_for='todos')
                            todo = todos[0]
                            assistant.speak(f"You can complete {todo['task']}")

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
                    playlists = assistant.player.get_playlists()
                    playlist = random.choice(playlists)
                    assistant.player.controller("playlist",playlist,'play')

                elif task == "control_player":
                    for word in controls:
                        if word in query:
                            assistant.player.send_request(word)

                elif task == 'news':
                    if entity is None:
                        entity = random.choice(news_interests)
                    news = assistant.automator.get_news(topic=entity)
                    assistant.speak(f"Here are some recent news related to {entity}")
                    for src,title in news.items():
                        assistant.speak(title + " source " + src)


                elif task == 'suggestions':
                    assistant.automator.suggestions(entity)

                elif task == 'bored':
                    response = random.choice(1,2)
                    if response == 1:
                        do =  webbrowser.open(random.choice(sites))
                        assistant.speak("How about this?")
                    else:
                        do = assistant.speak(brain.ask(question="I am bored"))

                elif task == 'get_weather':
                    assistant.automator.get_weather(entity)

                elif task == 'exit':
                    break
                
                else:
                    assistant.speak(random.choice(assistant.personality['dialogs']['misunderstand']))
                    print("I dont understand")
                    continue