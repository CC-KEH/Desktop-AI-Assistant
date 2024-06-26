from dotenv import load_dotenv
import os
from tools import *
from saved_data.constants import *
load_dotenv()

pdf_path = os.path.join(read_file_path)


tools = [
    note_engine_tool,
    file_reader_engine_tool,
]