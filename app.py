from flask import Flask, request, jsonify, render_template, url_for,send_from_directory
from gemini import generate_response
import sys
import os

app = Flask(__name__)

sys.stdout.reconfigure(encoding='utf-8')

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없다면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('sudal.html')

@app.route('/generate-ad', methods=['POST'])
def generate_ad():
    data = request.form
    ratio = data.get('ratio')
    style = data.get('style')
    subject = data.get('subject')
    requirement = data.get('requirement')
    image=request.files.get('image')

    if image and image.filename != '':
        filename=image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        image_url=url_for('uploaded_file', filename=filename)
        print(f"이미지 파일 전송 성공")
    else:
        print("이미지 파일이 전송되지 않았습니다.")

    print(f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}")

    gemini_cmd = "아래 내용을 참고해서 홍보 문구를 30자 내외로 작성해주세요."
    gemini_fmt = "설명은 하지말고 작성한 홍보 문구만 제출해주세요."

    message = gemini_cmd + f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}" + gemini_fmt
    response = {
        'message': generate_response(message),
        'image_url':image_url
    }
    print(response)

    return jsonify(response)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)