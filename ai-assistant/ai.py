import config
import os
import sys
from dotenv import load_dotenv
from llama_index.llms import OpenAI
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from prompts import *
from rag import tools
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
load_dotenv()


class Brain:
    def __init__(self):
        self.llm = OpenAI(model='gpt-3.5-turbo-0613')
        self.agent = ReActAgent.from_tools(
            tools, llm=self.llm, verbose=True, context=context_str)

    def ask(self, question):
        self.agent.query(question)
