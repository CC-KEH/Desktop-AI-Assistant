from utils import read_json
class Personality:
    def __init__(self):
        self.config = read_json('config.json')
        
    def upgrade_personality(self):
        pass
    
    def degrade_personality(self):
        pass
        