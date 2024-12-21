from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from qa_system import initialize_qa_system, ask_question

app = Flask(__name__)
CORS(app)

# 파일 업로드 설정
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없으면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# QA 시스템 초기화
qa_system = initialize_qa_system()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    try:
        # 텍스트 질문 받기 (선택사항)
        question = request.form.get('question', '')

        # 이미지 파일 처리
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)

        # 이미지만 있는 경우에도 QA 시스템에 전달
        answer = ask_question(qa_system, question or None, image_path)

        # 이미지 파일 처리 후 삭제
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# JSON 형식으로도 받을 수 있도록 추가 엔드포인트 유지
@app.route('/ask_json', methods=['POST'])
def ask_json():
    try:
        data = request.json
        question = data.get('question', '')
        answer = ask_question(qa_system, question or None)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)