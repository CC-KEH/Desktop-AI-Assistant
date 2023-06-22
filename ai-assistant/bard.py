from bardapi import Bard
from config import BARD_API
token = BARD_API
bard = Bard(token=token)
answer = bard.get_answer("who am i?")['content']
print(answer.encode("utf-8"))
