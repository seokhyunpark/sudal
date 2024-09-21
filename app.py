import ast
import sys

from add_text import add_image_text
from flask import Flask, request, jsonify, render_template
from gemini import generate_response
from io import BytesIO
from PIL import Image


sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

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
        #image.save(f"./uploads/")#uploads폴더 엇으면 오류
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

if __name__ == '__main__':
    app.run(debug=True)
