from flask import Flask, request, jsonify, render_template
from gemini import generate_response
import sys

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

    if image and image.filename != '':
        filename=image.filename
        #image.save(f"./uploads/")#uploads폴더 엇으면 오류
        print(f"이미지 파일 전송 성공")
    else:
        print("이미지 파일이 전송되지 않았습니다.")

    print(f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}")

    gemini_cmd = "아래 내용을 참고해서 홍보 문구를 30자 내외로 작성해주세요."
    gemini_fmt = "설명은 하지말고 작성한 홍보 문구만 제출해주세요."

    message = gemini_cmd + f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}" + gemini_fmt
    response = {'message': generate_response(message)}
    print(response)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
