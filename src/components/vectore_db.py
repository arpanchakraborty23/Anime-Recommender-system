import os, sys
from pathlib import Path
from dataclasses import dataclass
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from src.config.config import VectoreDBConfig
from src.utils.logger import logging
from src.utils.exeption import CustomException


from dotenv import load_dotenv
load_dotenv()

@dataclass
class VectoreDBArtifacts:
    vectore_db_path: Path

class VectorStoreBuilder:
    def __init__(self,csv_path:Path = None, config:VectoreDBConfig =None):
        self.csv_path = Path(csv_path)
        self.config= config
        self.embedding =HuggingFaceEmbeddings(model_name ="all-MiniLM-L6-v2")
    def build_and_save_vectorstore(self):
        try:
            print(self.csv_path)
            loader = CSVLoader(
                file_path=self.csv_path,
                encoding='utf-8',
                metadata_columns=[]
            )

            data = loader.load()

            splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
            texts = splitter.split_documents(data)

            os.makedirs(self.config.database_store_path,exist_ok=True)

            db = Chroma.from_documents(
                documents=texts,
                embedding=self.embedding,
                persist_directory=self.config.database_store_path
                )
            logging.info("vectore store completed")
      

            return VectoreDBArtifacts(self.config.database_store_path)
        
        except Exception as e:
            logging.error(f"Vectore store error: {e}")
            raise CustomException(e,sys)

def load_vector_store(path,embedding):
    db=Chroma(persist_directory=path,embedding_function=embedding)
    logging.info("Vectore database loaded")
    return db


