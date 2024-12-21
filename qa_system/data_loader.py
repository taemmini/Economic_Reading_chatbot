import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import logging


def load_documents(pdf_dir, text_dir):
    documents = []

    # Load PDF files
    if pdf_dir and os.path.isdir(pdf_dir):
        for pdf_file in os.listdir(pdf_dir):
            if pdf_file.lower().endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, pdf_file)
                try:
                    loader = PyPDFLoader(pdf_path)
                    loaded_docs = loader.load()
                    documents.extend(loaded_docs)
                    logging.info(f"Loaded PDF: {pdf_file}")
                except Exception as e:
                    logging.error(f"Error loading PDF {pdf_file}: {str(e)}")
    else:
        logging.warning(f"PDF directory does not exist or is not set: {pdf_dir}")

    # Load text files
    if text_dir and os.path.isdir(text_dir):
        for text_file in os.listdir(text_dir):
            if text_file.lower().endswith('.txt'):
                text_path = os.path.join(text_dir, text_file)
                try:
                    loader = TextLoader(text_path)
                    loaded_docs = loader.load()
                    documents.extend(loaded_docs)
                    logging.info(f"Loaded text file: {text_file}")
                except Exception as e:
                    logging.error(f"Error loading text file {text_file}: {str(e)}")
    else:
        logging.warning(f"Text directory does not exist or is not set: {text_dir}")

    return documents