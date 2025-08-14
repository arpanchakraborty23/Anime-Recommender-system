from src.components.data_ingestion import DataIngestion
from src.config.config import DataIngestionConfig

config =DataIngestionConfig()
obj = DataIngestion(config=config)
obj.load_and_process()