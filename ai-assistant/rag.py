from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from tools import *
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from llama_index.readers import PDFReader
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage, SimpleDirectoryReader
from constants import *
load_dotenv()

pdf_path = os.path.join(read_file_path)
obsidian_notes_path = os.path.join(obsidian_notes_path)
df_path = pd.read_csv(dfs_path)


tools = [
    note_engine_tool,
    dataframe_reader_engine_tool,
    file_reader_engine_tool,
    get_obsidian_reader_engine,
]
