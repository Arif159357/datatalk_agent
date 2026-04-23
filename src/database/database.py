import os

from langchain_community.utilities import SQLDatabase

from dotenv import load_dotenv

load_dotenv()

conn_str = os.getenv("DATABASE_URL")
datatalk_db = SQLDatabase.from_uri(conn_str, sample_rows_in_table_info=0)
