from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from prompts import pandas_prompt, instruction_str
from tools import *
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from constants import *

load_dotenv()

pdf_path = os.path.join(pdfs_path)
df_path = pd.read_csv(dfs_path)

df_query_engine = PandasQueryEngine(
    df=df_path, verbose=True, instruction_str=instruction_str)

df_query_engine.update_prompts({"pandas_prompt": pandas_prompt})

tools = [
    note_engine_tool,
    query_engine_tool,
]
