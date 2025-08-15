import os, sys
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config.config import VectoreDBConfig
from src.utils.logger import logging
from src.utils.exeption import CustomException


from dotenv import load_dotenv
load_dotenv()

class VectorStoreBuilder:
    def __init__(self,csv_path:Path, config:VectoreDBConfig):
        self.csv_path = csv_path
        self.config= config
        self.embedding = GoogleGenerativeAIEmbeddings(
            model=self.config.embedding_model,
            google_api_key=os.getenv("GIMINI_API_KEY")
        )
    def build_and_save_vectorstore(self):
        try:
            loader = CSVLoader(
                file_path=self.csv_path,
                encoding='utf-8',
                metadata_columns=[]
            )

            data = loader.load()

            splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
            texts = splitter.split_documents(data)

            os.makedirs(self.config.database_store_path,exist_ok=True)

            db = Chroma.from_documents(
                documents=texts,
                embedding=self.embedding,
                persist_directory=self.config.database_store_path
                )
            logging.info("vectore store completed")
            db.persist()
        except Exception as e:
            logging.error(f"Vectore store error: {e}")
            raise CustomException(e,sys)

    def load_vector_store(self):
        db=Chroma(persist_directory=self.config.database_store_path,embedding_function=self.embedding)
        logging.info("Vectore database loaded")
        return db


