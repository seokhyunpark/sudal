import sys
import os
import glob

from add_text import add_image_text
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from gemini import generate_response
from io import BytesIO
from PIL import Image

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

    # uploads 폴더의 모든 파일 삭제
    folder_path = './uploads'
    
    # 폴더 내의 모든 파일을 찾고 삭제
    files = glob.glob(os.path.join(folder_path, '*'))
    for file in files:
        try:
            os.remove(file)
            print(f"파일 삭제: {file}")
        except Exception as e:
            print(f"파일 삭제 오류: {e}")

    data = request.form
    ratio = data.get('ratio')
    style = data.get('style')
    subject = data.get('subject')
    requirement = data.get('requirement')
    image=request.files.get('image')

    print(f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}")

    gemini_cmd = ("""
    아래 내용을 참고해서 이모티콘을 사용하지 않고 텍스트 문자로만 홍보 문구를 작성해주세요.
    15자 내외의 짧은 문구를 1개 작성해주세요.
    """
    )
    gemini_fmt = ("다른 설명은 필요없고 홍보 문구만 작성해주세요. 이모티콘은 절대로 사용하지마세요.")

    message = gemini_cmd + f"비율: {ratio}, 스타일 {style}, 주제: {subject}, 요구 사항: {requirement}" + gemini_fmt
    phrase = generate_response(message).rstrip()

    if image and image.filename != '':
        filename=image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        
        print(f"이미지 파일 전송 성공")

        with open(image_path, 'rb') as img_file:
            image_file = img_file.read()

        image = Image.open(BytesIO(image_file))
        image = add_image_text(image, phrase)
        image.save(f"./uploads/001.png")

    else:
        print("이미지 파일이 전송되지 않았습니다.")

    response = {
        'message': phrase,
        'image_url' : url_for('uploaded_file', filename="001.png")
        }
    print(response)


    return jsonify(response)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)