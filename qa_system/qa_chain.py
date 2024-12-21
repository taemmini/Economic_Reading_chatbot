from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import logging
from .config import openai_api_key
from .image_processor import ImageProcessor

# Constants
DEFAULT_MODEL = "gpt-4o-2024-11-20"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_IMAGE_PROMPT = "You're an helpful AI who can answer questions in a image format. Read the image and give me an answer about the question. While answering, you have to retrieve information from the vector database provided. You have to answer in Korean. Just answer the question, don't explain the process."
DEFAULT_TOP_P = 1

class QASystem:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.text_qa_chain = self._create_text_qa_chain()
        self.image_processor = ImageProcessor(openai_api_key)

    def _create_text_qa_chain(self):
        try:
            llm = ChatOpenAI(
                model_name=DEFAULT_MODEL,
                openai_api_key=openai_api_key,
                temperature=DEFAULT_TEMPERATURE,
                top_p=DEFAULT_TOP_P
            )
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever()
            )
        except Exception as e:
            logging.error(f"Text QA 체인 생성 실패: {str(e)}")
            raise

    def process_query(self, query: str = None, image_path: str = None):
        """Process query with text and/or image input"""
        if not query and not image_path:
            raise ValueError("쿼리나 이미지 중 하나는 제공되어야 합니다")

        try:
            if image_path:
                image_response = self.image_processor.process_image(
                    image_path,
                    query or DEFAULT_IMAGE_PROMPT
                )
                if not query:
                    return image_response
                    
                text_response = self.text_qa_chain.run(query)
                return f"정답은: {image_response}"
            
            return self.text_qa_chain.run(query)

        except Exception as e:
            logging.error(f"쿼리 처리 중 오류 발생: {str(e)}")
            raise