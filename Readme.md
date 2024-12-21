# 경제학 강의 챗봇 프로젝트

## 소개
이 프로젝트는 경제학 강의 내용을 기반으로 한 AI 챗봇 시스템입니다. 사용자는 텍스트나 이미지를 통해 질문을 할 수 있으며, OpenAI의 GPT 모델을 활용하여 답변을 제공합니다.

## 주요 기능
- 텍스트 기반 Q&A
- 이미지 업로드 및 분석
- 드래그 앤 드롭 이미지 업로드
- 실시간 채팅 인터페이스

## 기술 스택
- **백엔드**: Flask, Python
- **프론트엔드**: HTML, JavaScript, TailwindCSS
- **AI/ML**: LangChain, OpenAI GPT
- **데이터베이스**: ChromaDB (벡터 저장소)
- **배포**: Docker, Nginx

## 설치 방법

1. 저장소 클론
```bash
git clone [repository-url]
```

2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정하세요:
```
OPENAI_API_KEY=your_api_key
PDF_DIRECTORY=path_to_pdf_dir
TEXT_DIRECTORY=path_to_text_dir
```

## 실행 방법

개발 서버 실행:
```bash
python app.py
```

## 프로젝트 구조
```
.
├── app.py                 # Flask 애플리케이션 메인 파일
├── qa_system/            # QA 시스템 관련 모듈
├── static/              # 정적 파일 (CSS, JS)
├── templates/           # HTML 템플릿
├── uploads/            # 임시 이미지 업로드 폴더
└── data/               # 학습 데이터
```

## API 엔드포인트

### `/ask` (POST)
- 질문을 처리하고 답변을 반환하는 엔드포인트
- 요청 형식:
  - `question`: 텍스트 질문 (선택사항)
  - `image`: 이미지 파일 (선택사항)

## 도커 배포

1. 도커 이미지 빌드:
```bash
docker-compose build
```

2. 컨테이너 실행:
```bash
docker-compose up -d
```

## 라이선스
이 프로젝트는 MIT 라이선스 하에 있습니다.

## 기여 방법
1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 주의사항
- 이 챗봇은 교육 목적으로 개발되었으며, 답변의 정확성을 100% 보장하지 않습니다.
- 민감한 개인정보는 입력하지 마세요.
- 이미지 업로드 시 허용된 확장자만 사용하세요 (png, jpg, jpeg, gif, webp).
