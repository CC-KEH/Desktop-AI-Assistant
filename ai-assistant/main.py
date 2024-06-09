import time
import random
import threading

from tools.utils import *
from tools.handlers import *
from personality.chat import *
from personality.dialogs import dialogs
from automation.modes_routines import Mode, Routine
# from tools.gesture_recognition import GestureRecognition

class Assistant:
    def __init__(self):
        self.utils = Utils()
        self.mode = Mode()
        self.routine = Routine()
        self.dialogs = dialogs
        
    def speak(self, text):
        self.utils.say(text)

    def listen(self, prompt=None):
        self.speak(prompt)
        self.utils.take_command()

    def set_mode(self,mode):
        modes = ['study', 'work', 'game', 'sleep']
        if mode in modes:
            if mode == 'study':
                self.mode.study_mode()
                
            if mode=='work':
                self.mode.work_mode()
                
            elif mode=='game':
                self.mode.game_mode()
            else:
                self.mode.sleep_mode()
                run = False
    
    def set_routine(self,routine):
        if routine == 'morning':
            self.routine.morning()
        else:
            self.routine.night()

def start_assistant():
    assistant = Assistant()
    assistant_name = 'Makima'
    start_time = time.time()
    news_time = time.time()
    run = True
    while run:
        print("Listening...")
        check_news(news_time)

        run = check_sleep(start_time)
        
        query = assistant.utils.take_command()
        
        if query:
            
            if query == 'exit':
                    break
                
            if 'hey' in query:
                print("replace hey")
                query = query.replace('hey', '')
            
            query = query.replace(assistant_name, '')
            
            model_response = get_response(query)
            
            if model_response[0]:
                assistant.speak(model_response[1])
                continue
            
            else:
                task = model_response[1]
                
                if task in ['study', 'work', 'games', 'nap']:
                    assistant.set_mode(mode=task)
                
                elif task in ['morning_routine', 'night_routine']:
                    assistant.set_routine(routine=task)
                        
                elif task == 'organise':
                    handle_organise()

                elif task in ['ask_gemini', 'ask_question']:
                    handle_ask_question(query=query)
                    
                elif task == "open_site":
                    handle_open_site(query=query)

                elif task == "set_reminder":
                    handle_set_reminder()
                    
                elif task == "send_mails":
                    handle_send_mails()
                            
                elif task=="get_mails":
                    handle_get_mails()
                
                elif task =='notion':
                    handle_notion(query=query)

                elif task == 'send_message':
                    handle_send_message()

                elif task == 'search':
                    handle_search()
                    
                elif task == 'run_program':
                    handle_run_program(query=query)

                elif task == "games":
                    handle_games(query=query)
                    
                elif task == 'play_music':
                    handle_play_music(query=query)

                elif task == "control_player":
                    handle_control_player(query=query)

                elif task == 'news':
                    handle_news(query=query)

                elif task == 'bored':
                    handle_bored()
                    
                else:
                    assistant.speak(random.choice(assistant.dialogs['misunderstand']))
                    print("I dont understand")
                    continue
    
def main():
    # gesture_recognition = GestureRecognition()

    # thread1 = threading.Thread(target=start_assistant)
    # thread2 = threading.Thread(target=gesture_recognition.read_gesture)

    # thread1.start()
    # thread2.start()

    # while True:
    #     pass
    pass

if __name__ == "__main__":
    start_assistant()