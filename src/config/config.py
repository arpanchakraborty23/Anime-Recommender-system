from pathlib import Path
from src.constants import (Data_Dir, Output_Data_File_Name, Input_Data_File_Name, required_cols,Database_Dir,Embedding_Model)

class DataIngestionConfig:
    def __init__(self) -> None:
        self.input_file_path = Path(Data_Dir) / Input_Data_File_Name
        self.output_file_path = Path(Data_Dir) / Output_Data_File_Name
        self.required_cols = required_cols.copy()

class VectoreDBConfig:
    def __init__(self) -> None:
        self.database_store_path = Database_Dir
        self.embedding_model = Embedding_Model