import json
import random
personality = json.load(open('personality.json', 'r'))
print(random.choice(personality['dialogs']['sleep']))