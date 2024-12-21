from .config import openai_api_key, pdf_dir, text_dir
from .data_loader import load_documents
from .text_processor import split_documents
from .vector_store import create_vector_store
from .qa_chain import QASystem
from .image_processor import ImageProcessor
import logging


def initialize_qa_system():
    try:
        # Step 1: Load documents
        documents = load_documents(pdf_dir, text_dir)

        # Step 2: Split documents into chunks
        texts = split_documents(documents)

        # Step 3: Create vector store
        vectorstore = create_vector_store(texts)

        # Step 4: Create QA system (includes both text and image processing)
        qa_system = QASystem(vectorstore)

        return qa_system

    except Exception as e:
        logging.error(f"Error initializing QA system: {str(e)}")
        raise


def ask_question(qa_system, question=None, image_path=None):
    """
    질문을 처리하고 답변을 반환합니다.

    Args:
        qa_system: QASystem 인스턴스
        question (str, optional): 사용자의 질문
        image_path (str, optional): 이미지 파일 경로

    Returns:
        str: 답변 텍스트
    """
    try:
        answer = qa_system.process_query(question, image_path)
        return answer
    except Exception as e:
        logging.error(f"Error during question answering: {str(e)}")
        if "maximum context length" in str(e):
            return "죄송합니다. 질문이 너무 길거나 복잡합니다. 더 간단한 질문으로 다시 시도해주세요."
        elif "api_key" in str(e).lower():
            return "API 키 설정에 문제가 있습니다. 관리자에게 문의해주세요."
        elif "image" in str(e).lower():
            return "이미지 처리 중 오류가 발생했습니다. 이미지 형식과 크기를 확인해주세요."
        else:
            return f"죄송합니다. 질문에 답변하는 중 오류가 발생했습니다: {str(e)}"