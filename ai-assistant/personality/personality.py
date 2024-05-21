from utils import read_json
import json
from personality.chat import get_response

class Personality:
    def __init__(self):
        self.personality = read_json('personality.json')

    def predict(self, message):
        response = get_response(message)
        print(response)
        return response