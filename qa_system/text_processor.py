from langchain.text_splitter import CharacterTextSplitter
import logging

def split_documents(documents):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    logging.info(f"Total text chunks after splitting: {len(texts)}")
    return texts