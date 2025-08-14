from pathlib import Path
from src.constants import Artifacts, Data_Dir, Output_Data_File_Name, Input_Data_File_Name, required_cols

class DataIngestionConfig:
    def __init__(self) -> None:
        self.input_file_path = Path(Data_Dir) / Input_Data_File_Name
        self.output_file_path = Path(Data_Dir) / Output_Data_File_Name
        self.required_cols = required_cols.copy()
