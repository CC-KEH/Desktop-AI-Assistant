from dotenv import load_dotenv
import os
import pandas as pd
from tools import *
from saved_data.constants import *
load_dotenv()

pdf_path = os.path.join(read_file_path)
df_path = pd.read_csv(dfs_path)


tools = [
    note_engine_tool,
    # dataframe_reader_engine_tool,
    file_reader_engine_tool,
]