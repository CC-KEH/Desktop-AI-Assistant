from bardapi import Bard
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import config
api_key = config.BARD_API

class Ai:
    def bard(self,question):
        token = api_key
        bard = Bard(token=token)
        answer = bard.get_answer(question)['content']
        return answer.encode("utf-8")


