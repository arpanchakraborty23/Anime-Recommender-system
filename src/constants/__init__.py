import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY= os.getenv("GIMINI_API_KEY")
LLM_MODEL="gemini-2.5-pro"

HF_API_KEY= os.getenv("HF_API_KEY")

Artifacts: str ="Artifacts"

## Data Ingestion Config
Data_Dir :str ="data"
Input_Data_File_Name :str = "anime-dataset-2023.csv"

Output_Data_File_Name: str = "process_data.csv"

required_cols : list[str] =["Name","Score","Genres","Synopsis","Episodes","Aired"]
