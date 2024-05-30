from saved_data.config import gemini_key
import os
import sys
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.gemini import Gemini
from prompts import *
from tools.rag import tools

os.environ["GOOGLE_API_KEY"] = gemini_key

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
load_dotenv()

class Brain:
    def __init__(self):
        self.llm = Gemini(model="models/gemini-pro",)
        self.agent = ReActAgent.from_tools(
            tools, llm=self.llm, verbose=True, context=context_str)
        
    def ask(self, question):
        response = self.agent.query(question)
        return response.text