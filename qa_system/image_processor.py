# qa_system/image_processor.py
import base64
from typing import Union, List
import os
import logging
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from PIL import Image
import io

# Constants
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0
DEFAULT_MODEL = "gpt-4o-2024-11-20"

class ImageProcessor:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model=DEFAULT_MODEL,
            api_key=api_key,
            max_tokens=DEFAULT_MAX_TOKENS,
            temperature=DEFAULT_TEMPERATURE
        )

    @staticmethod
    def encode_image(image_path: str) -> str:
        """이미지를 base64로 인코딩"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logging.error(f"이미지 인코딩 실패: {str(e)}")
            raise

    def process_image(self, image_path: str, query: str) -> str:
        """이미지와 질문을 처리하여 응답 생성"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

        try:
            base64_image = self.encode_image(image_path)
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }]

            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:
            logging.error(f"이미지 처리 실패: {str(e)}")
            raise