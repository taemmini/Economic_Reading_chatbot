from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import logging
from .config import openai_api_key

def create_vector_store(texts):
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=openai_api_key)
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            collection_name="Readings_in_Economics_Final_Exam",
        )
        logging.info("Vector store created successfully with larger embeddings")
        return vectorstore
    except Exception as e:
        logging.error(f"Error creating vector store with larger embeddings: {str(e)}")
        raise