import sys
import os
import glob
import ast

from add_text import add_image_text
from flask import Flask, request, jsonify, render_template
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

    gemini_cmd = ("아래 내용을 참고해서 홍보 문구를 작성해주세요."
                  "이모티콘은 사용하지말고 20자 내외의 짧은 문구를 총 5개 작성해주세요.")
    gemini_fmt = ("파이썬의 리스트 형태만 작성해주세요. 예시: ['문구1', '문구2', '문구3', '문구4', '문구5']"
                  "리스트 이외의 값, '''python 등 다른 글자는 작성하지 말아주세요.")

    message = gemini_cmd + f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}" + gemini_fmt
    response = {'message': generate_response(message)}
    print(response)

    if image and image.filename != '':
        filename=image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        image_url=url_for('uploaded_file', filename=filename)
        print(f"이미지 파일 전송 성공")

        image_file = image.read()

        response_in_list = ast.literal_eval(response['message'])
        
        file_names = ["001", "002", "003", "004", "005"]
          
        i = 0
        for text in response_in_list:
            image = Image.open(BytesIO(image_file))
            image = add_image_text(image, text)
            image.save(f"./uploads/{file_names[i]}.png")
            i += 1

    else:
        print("이미지 파일이 전송되지 않았습니다.")


    return jsonify(response)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)