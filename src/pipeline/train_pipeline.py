from src.components.data_ingestion import DataIngestion
from src.components.vectore_db import VectorStoreBuilder
from src.config.config import DataIngestionConfig, VectoreDBConfig

class TrainPipeline:
    def __init__(self) -> None:
        pass

    def run_pipeline(self):
        data_ingestion_config =DataIngestionConfig()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion_artifact=data_ingestion.load_and_process()
        print(data_ingestion_artifact)

        vector_db_config = VectoreDBConfig()
        vector_db = VectorStoreBuilder(
            csv_path=data_ingestion_artifact.output_file_path,
            config=vector_db_config
        )

        vector_db.build_and_save_vectorstore()
        print("Pipeline Run Successfully !")
                

