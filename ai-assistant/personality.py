from utils import read_json
import json
class Personality:
    def __init__(self):
        self.personality = read_json('personality.json')
    
        