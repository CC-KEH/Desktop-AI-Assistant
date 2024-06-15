import os
import json
import time
import random
import webbrowser
import datetime
from saved_data.constants import *
from personality.dialogs import dialogs
from automation.automation import Automation
from connections.brain import Brain
from connections.player import SpotipyPlayer
from connections.notion import Notion
from connections.google import Google
from connections.brain import Brain
from tools.utils import Utils, process_datetime
from tools.organise import Organiser

utils_obj = Utils()
automation_obj = Automation()
brain_obj = Brain()
player_obj = SpotipyPlayer()
organiser_obj = Organiser()
brain_obj = Brain()

def speak(text:str):
    utils_obj.say(text)

def listen(prompt:str):
    speak(prompt)
    command = utils_obj.take_command()
    return command.lower()

def prepare_message(recipient_name):
    with open('../saved_data/contacts.json', 'r') as f:
        contacts = json.load(f)
    try:
        recipient_no = contacts[recipient_name]
        if recipient_no is None:
            print("Recipient not found.")
            return
        message = listen("What message do you want to send?")
        time = listen("What time do you want to send the message?")
        if "now" in time:
            time = datetime.datetime.now()
        utils_obj.say("Okay, I will send message to " + recipient_name + " at " + str(time))
        automation_obj.send_message(phone_no=recipient_no, time=time, message=message, code='+91')
    
    except KeyError as e:
        print("New contact")
        print("What is the phone number of the recipient?")
        no = input()
        contacts[recipient_name] = no
        with open('contacts.json', 'w') as f:
            json.dump(contacts, f)
        prepare_message(recipient_name)
    
    
#**********************************************#
#****************** Handlers ******************#
#**********************************************#

def handle_organise():
    try:
        with open(organised_path, "r") as file:
            last_organised = file.readlines()
            if len(last_organised) > 0:
                last_organised = last_organised[-1]
                last_organised = last_organised.replace("\n", "")
                last_organised = datetime.datetime.strptime(
                    last_organised, "%Y-%m-%d %H:%M:%S.%f"
                )
                if (datetime.datetime.now() - last_organised).days < 7:
                    response = listen("Files were already organised this week. Do you want to organise again?")
                    if "no" in response.lower():
                        return
            if not os.path.exists(base_path):
                utils_obj.say("You have not yet set a base path for me.")
                
            else:
                organiser_obj.organise()
                utils_obj.say("Files have been organised successfully.")

    except FileNotFoundError:
        utils_obj.say("Organised logs file not found.\n Organising files for the first time.")
        with open(organised_path, 'w') as fp:
            fp.write(str(datetime.datetime.now()) + "\n")
            organiser_obj.organise()

def handle_ask_question(query=None):
    if query is None:
        query = listen("What is your question about?")
    print("Called Gemini")
    utils_obj.say(brain_obj.ask(question=query))

def handle_open_site(query):
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            utils_obj.say(f"opening {site[0]}")
            webbrowser.open(f"{site[1]}")

def handle_set_reminder():
    google_obj = Google()
    start_date = process_datetime(isstart = True)
    end_date = process_datetime(isstart = False)
    summary = listen("What should I remind you about?")
    description = listen("Any additional information?")
    location = listen("Location?")
    utils_obj.say("okaey, hangon a second")
    google_obj.create_event(start_date, end_date, summary, location, description)

def handle_get_mails():
    google_obj = Google()
    mails = google_obj.get_mails()
    if mails is None:
        utils_obj.say("I could not fetch the mails")
    else:
        for mail in mails:
            utils_obj.say(f"{mail[0]}  {mail[1]}")

def handle_send_mails():
    google_obj = Google()
    to = listen("Who do you want to send the mail to?")
    subject = listen("What is the subject of the mail?")
    mail_text = listen("What is the mail?")
    google_obj.send_mail(to, subject, mail_text)

def handle_notion(query):
    notion_obj = Notion()
    
    if 'notion' in query:
        query = query.replace('notion','')
        
    if 'movie' or 'movies' in query:
        movies = notion_obj.get_data(asked_for='movies')
        movie = random.choice(movies)
        utils_obj.say(f"You can watch {movie['name']}")
    
    elif 'book' or 'books' in query:
        books = notion_obj.get_data(asked_for='books')
        book = random.choice(books)
        utils_obj.say(f"You can read {books['name']}")
    
    elif 'anime' or 'animes' in query:
        animes = notion_obj.get_data(asked_for='animes')
        anime = random.choice(animes)
        utils_obj.say(f"You can watch {animes['name']}")
    
    elif 'task' or 'tasks' in query:
        query = query.replace('task','')
        todos = notion_obj.get_data(asked_for='todos')
        found = False
        if 'mark' in query:
            query = query.replace('mark','')
            task = None
            for word in query.split():
                for todo in todos:
                    print(word,todo['task'])
                    if (word == todo['task']):
                        task = todo
                        print("found")
                        found = True
                        break
                    
                if found:
                    break
                
            if task is None:
                utils_obj.say("I could not find the task you are talking about")
                
            else:
                notion_obj.update_item(item=task, asked_for='todos')
                utils_obj.say(f"Marked {todo['task']} as complete")
                
        else:
            todos = notion_obj.get_data(asked_for='todos')
            todo = todos[0]
            utils_obj.say(f"You can complete {todo['task']}")

def handle_send_message():
    recipient_name  = listen("Who do you want to send a message to?")
    prepare_message(recipient_name)

def handle_search():
    search_term = listen("What do you want to search for?")
    automation_obj.search(search_term)

def handle_run_program(query):
    if 'run' in query:
        query = query.replace('run','')
    if 'program' in query:
        query = query.replace('program','')
    
    utils_obj.run_program(query, third_party=True)

def handle_games(query=None):
    if 'open' in query:
        query = query.replace('open','')
    query = query.strip()
    if query is None:
        game = random.choice(list(games.keys()))
        utils_obj.say(f"How about {game}")
        utils_obj.run_program(game, third_party=True)
    else:
        utils_obj.run_program(query, third_party=True)
        
def handle_play_music(query=None):
    if 'some' or 'something' in query:
        playlists = player_obj.get_playlists()
        playlists = player_obj.format_playlists(playlists)
        print(playlists)
        player_obj.play_playlist(random.choice(playlists)[0])
    else:
        if 'play' in query:
            query = query.replace('play','')
        if 'song' in query:
            query = query.replace('song','')
        song_name = query
        song = player_obj.search(song_name)
        print(song)
        player_obj.play(song)

def handle_control_player(query=None):
    for word in controls:
        if word in query:
            if word == 'play':
                player_obj.play()
            elif word == 'pause':
                player_obj.pause()
            elif word == 'next':
                player_obj.next()
            elif word == 'previous':
                player_obj.previous()
            elif word == 'seek':
                pass
            elif word == 'repeat':
                pass
            elif word == 'shuffle':
                pass

def handle_news(query=None):
    if query is None:
        query = random.choice(news_interests)
    news = automation_obj.get_news(topic=query)
    utils_obj.say(f"Here are some recent news related to {query}")
    for src,title in news.items():
        utils_obj.say(title + " source " + src)

def handle_bored():
    response = random.choice([1,2])
    if response == 1:
        site = random.choice(sites)
        do =  webbrowser.open(site[1])
        utils_obj.say("How about this?")
    else:
        do = utils_obj.say(brain_obj.ask(question="I am bored"))

def check_news(news_time):
    if (time.time() - news_time) > (3600*2):
        topic = random.choice(news_interests)
        news = automation_obj.get_news(topic=topic)
        utils_obj.say(f"Here are some recent news related to {topic}")
        for src,title in news.items():
            utils_obj.say(title + " source " + src)
        news_time = time.time()
        
def check_sleep(start_time):
    if (time.time() - start_time) > (3600*5):
        utils_obj.say(random.choice(dialogs['sleep']))
        return False
    else:
        return True