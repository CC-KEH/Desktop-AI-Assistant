import os
import sys
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.gemini import Gemini
from saved_data.prompts import *
from tools.rag import tools

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("gemini_api_key")

class Brain:
    def __init__(self):
        self.llm = Gemini(model="models/gemini-pro",)
        self.agent = ReActAgent.from_tools(
            tools, llm=self.llm, verbose=True, context=context_str)
        
    def rag(self, question):
        response = self.agent.query(question)
        return response.text
    
    def ask(self,question):
        response = self.llm.complete(question)
        return response
    
if __name__ == '__main__':
    brain = Brain()
    context = context_str
    question = "What is your name?"
    print(brain.ask(f"{context},+question: {question}"))
    rag_question = "What is a RAG?"
    brain.rag(f"question: {rag_question}")