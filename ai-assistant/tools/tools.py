from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os
from saved_data.constants import *

query_question = ""
query_topic = ""


def save_note(note,topic):
    note_file = os.path.join(notes_path, f'{topic}_notes.txt')
    if not os.path.exists(note_file):
        open(note_file, 'w')

    with open(note_file, 'a') as f:
        f.writelines([note + '\n'])

    return 'created notes and saved them'


def get_reader_engine():
    document = SimpleDirectoryReader('read_file_path').load_data()
    index = VectorStoreIndex.from_documents(document, show_progress=True)
    query_engine = index.as_query_engine()
    query_engine_tool = QueryEngineTool(
        query_engine=query_engine, metadata=ToolMetadata(
            name=f'{query_topic}', description=f'This gives detailed information about {query_question}')
    )
    return query_engine_tool

note_engine_tool = FunctionTool.from_defaults(
    fn=save_note,
    name='note_saver',
    description='this tool can save a text based note to a file for the user. It takes in a note and a topic as arguments. The note is saved to a file with the topic as the filename.'
)

file_reader_engine_tool = get_reader_engine()