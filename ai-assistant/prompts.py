from llama_index.core import PromptTemplate
from utils import *


personality = read_json('personality.json')
task = "Help the user with their query, and provide them with the necessary information, guidance, and if need be, the tools to complete their task."

context_str = f"""
    Your Personality is: {personality}
    What you are asked to do: {task}
"""

instruction_str = """
1.
"""

query_str = ""

pandas_prompt = PromptTemplate(
    f"""
    {context_str}
    Follow these instructions:
    {instruction_str}
    Query: {query_str}

    Expression: 
    """
)
