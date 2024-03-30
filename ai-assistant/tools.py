from llama_index.tools import FunctionTool, QueryEngineTool, ToolMetadata
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from prompts import pandas_prompt, instruction_str
import os
from constants import *
note_file = os.path.join(notes_path, 'notes.txt')

query_question = ""
query_topic = ""


def save_note(note):
    if not os.path.exists(note_file):
        open(note_file, 'w')

    with open(note_file, 'a') as f:
        f.writelines([note + '\n'])

    return note_save_return_response_successful


def get_query_engine():
    df_query_engine = PandasQueryEngine(
        df=df_path, verbose=True, instruction_str=instruction_str)

    df_query_engine.update_prompts({"pandas_prompt": pandas_prompt})
    return QueryEngineTool(query_engine=df_query_engine, metadata=ToolMetadata(
        name=f'{query_topic}',
        description=f'This gives information about {query_question}'
    ))


note_engine_tool = FunctionTool.from_defaults(
    fn=save_note,
    name='note_saver',
    description='this tool can save a text based note to a file for the user'
)

query_engine_tool = get_query_engine()
