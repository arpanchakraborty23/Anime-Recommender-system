import os, sys
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from src.prompt import get_anime_prompt
from src.utils.logger import logging
from src.utils.exeption import CustomException
from src.components.vectore_db import load_vector_store
from src.constants import Embedding_Model
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings

class AnimeRecommender:
    def __init__(self):

        embedding =HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GIMINI_API_KEY"),
            temperature=0
        )

        # load db
        db = load_vector_store(path="db",embedding=embedding)

        self.prompt = get_anime_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def invoke(self, query: str):
        try:
            result = self.qa_chain.invoke({"query": query})
            return result["result"]
        except Exception as e:
            logging.error(f"Error to get recommendation: {e}")
            raise CustomException(e, sys)
