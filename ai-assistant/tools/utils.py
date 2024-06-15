import screen_brightness_control as sbc
import speech_recognition as sr
import win32com.client
import subprocess
from box import ConfigBox 
import json
from fuzzywuzzy import fuzz
import spacy 
import os
from datetime import datetime

from saved_data.constants import applications, games

nlp = spacy.load("en_core_web_sm")
class Utils:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        # Get the list of available voices
        voices = self.speaker.GetVoices()  
        # Loop through the voices to find the Catherine voice
        for voice in voices:
            if 'Zira' in voice.GetDescription():
                self.speaker.Voice = voice
                break
    
    def say(self,text):
        self.speaker.speak(f"{text}") 
    
    def run_program(self, query, third_party=False):
        if not third_party:
            try:
                # Execute a system command to find the program path
                result = subprocess.run(['where', query], capture_output=True, text=True)
                output = result.stdout.strip()

                if output:
                    program_path = output.split('\n')[0]
                    self.say(f'opening {query}')
                    subprocess.Popen(program_path)
                    print(f"Opened {query} successfully!")
                else:
                    print(f"Program '{query}' not found.")

            except OSError as e:
                print(f"Error opening {query}: {e}")
            
        else:
            if query in applications.keys():
                subprocess.run(['powershell', '-Command', applications[query]])
            elif query in games.keys():
                subprocess.run(['powershell', '-Command', games[query]])
            else:
                self.say("I cant find the program.")
    

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio,language='en-in')
                print(f'User: {query}')
                return query
            except Exception as e:
                return "Sorry, I could'nt catch what you were saying."


def read_json(file_path)->ConfigBox:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return ConfigBox(data)


def find_best_match(query, items):
    print("query",query)
    best_match = None
    highest_score = 0
    for item in items:
        name = item
        score = fuzz.ratio(query.lower(), name.lower())
        if score > highest_score:
            highest_score = score
            best_match = item
            
    return best_match

def search_file(directory, filename):
    for dirpath, dirnames, files in os.walk(directory):
        if filename in files:
            return os.path.join(dirpath, filename)
    return None


def control_brightness(level=100, display=0):
    # brightness = sbc.get_brightness()
    # primary = sbc.get_brightness(display=display)
    sbc.set_brightness(level, display=display)


# 1 - > Year
# 2 - > Month
# 3 - > Day
def get_str_to_int(item,asked_for,isstart):
    item = item.strip()
    try:
        if asked_for==1:
            if item.isdigit():
                if len(item) == 2:
                    return int(f"20{item}")
                return int(item)
            else:
                year = item.lower()
                year_to_num = {
                'twenty four': 2024,
                'twenty five': 2025,
                'twenty six': 2026,
                'twenty seven': 2027,
                'twenty eight': 2028,
                'twenty nine': 2029,
                'thirty': 2030,
                }
                if year == "this year" or year == "current":
                    return datetime.now().year

                year_name = find_best_match(year, list(year_to_num.keys()))
                return year_to_num.get(year_name, None)

        elif asked_for==2:
            month = item.lower()
            month_to_num = {
                'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6,
                'july': 7,
                'august': 8,
                'september': 9,
                'october': 10,
                'november': 11,
                'december': 12
            }
            month_name = find_best_match(month, list(month_to_num.keys()))
            if month == "this month" or month == "current":
                return datetime.now().month
            else:
                return month_to_num.get(month_name, None)
        else:
            day = item
            day_to_no = {
                'today': datetime.now().day,
                'tomorrow': datetime.now().day + 1,
                'day after tomorrow': datetime.now().day + 2,
                "first": 1,"second": 2,"third": 3,"4th": 4,"5th": 5,"6th": 6,"7th": 7,
                "8th": 8,"9th": 9,"10th": 10,"11th": 11,"12th": 12,"13th": 13,
                "14th": 14,"15th": 15,"16th": 16,"17th": 17,"18th": 18,"19th": 19,"20th": 20,
                "21st": 21,"22nd": 22,"23rd": 23,"24th": 24,"25th": 25,"26th": 26,"27th": 27,
                "28th": 28,"29th": 29,"30th": 30,"31st": 31
            }
            if day == "today" or day == "now":
                return datetime.now().day

            day = find_best_match(day, list(day_to_no.keys()))
            return day_to_no.get(day, None)
    
    except Exception as e:
        print(e)
        process_datetime(isstart)
    
def process_datetime(isstart):
    utils = Utils()
    if isstart:
        utils.say("Tell the start date and time: ")
    else:
        utils.say("Tell the end date and time: ")
    year = datetime.now().year
        
    date_input = utils.take_command().lower()

    # Split input into day and month
    day, month = date_input.split()
    print("Day:",day,"Month:",month)
    
    # Convert day and month to numerical values
    day = get_str_to_int(item=day,asked_for=3,isstart=isstart)
    month = get_str_to_int(item=month, asked_for=2,isstart=isstart)
    
    print("Day:",day,"Month:",month)
    
    # Set time to 00:00:00
    hour = 00
    minute = 00
    second = 00
    
    # Format datetime string
    datetime_str = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

    # Validate and convert to datetime object
    try:
        # datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
        # print(f"Converted datetime: {datetime_obj}")
        # return datetime_obj
        return datetime_str
    except ValueError:
        print("Invalid date or time format. Please try again.")
        process_datetime(isstart)