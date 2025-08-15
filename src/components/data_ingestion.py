import sys,os
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from src.config.config import DataIngestionConfig
from src.utils.logger import logging
from src.utils.exeption import CustomException  # fixed spelling

@dataclass
class DataIngestionArtifacts:
    output_file_path: Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config

    def load_and_process(self) -> DataIngestionArtifacts:
        try:
            # Load CSV
            df = pd.read_csv(self.config.input_file_path)
            logging.info(f"Data loaded successfully: {df.shape}")

            # Drop NaNs if any
            if df.isnull().values.any():
                df = df.dropna()

            logging.info(f"Col:{df.columns}")
            # Check required columns
            if not all(col in df.columns for col in self.config.required_cols):
                raise ValueError("Some required columns are missing in CSV file")

            # Create combined column
            df['combine_info'] = (
                "Title:" + df["Name"].astype(str)
                + " Score:" + df["Score"].astype(str)
                + " Genres:" + df['Genres'].astype(str)
                + " Synopsis:" + df["Synopsis"].astype(str)
                + " Episodes:" + df["Episodes"].astype(str)
                + " Aired:" + df["Aired"].astype(str)
            )

            # Ensure the folder exists
            self.config.output_file_path.parent.mkdir(parents=True, exist_ok=True)
            # Save output (entire DataFrame)
            df['combine_info'][:500].to_csv(self.config.output_file_path, index=False)
            logging.info(f"Processed data saved at: {self.config.output_file_path}")

            return DataIngestionArtifacts(self.config.output_file_path)

        except Exception as e:
            logging.error(str(e))
            raise CustomException(e, sys)
