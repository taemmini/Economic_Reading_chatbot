# qa_system/config.py
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI API Key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Directories for PDF and text files
pdf_dir = os.getenv('PDF_DIRECTORY')
text_dir = os.getenv('TEXT_DIRECTORY')

# 추가 확인 로그
if pdf_dir:
    logging.info(f"PDF Directory set to: {pdf_dir}")
else:
    logging.warning("PDF Directory not set or not found in .env file.")

if text_dir:
    logging.info(f"Text Directory set to: {text_dir}")
else:
    logging.warning("Text Directory not set or not found in .env file.")
