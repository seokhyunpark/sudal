from flask import Flask, request, jsonify, render_template
from gemini import generate_response


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sudal.html')

@app.route('/generate-ad', methods=['POST'])
def generate_ad():
    data = request.json
    ratio = data.get('ratio')
    style = data.get('style')
    subject = data.get('subject')
    requirement = data.get('requirement')
    print(f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}")

    gemini_cmd = "아래 내용을 참고해서 홍보 문구를 30자 내외로 작성해주세요."
    gemini_fmt = "설명은 하지말고 작성한 홍보 문구만 제출해주세요."

    message = gemini_cmd + f"비율: {ratio},  스타일 {style}, 주제: {subject}, 요구 사항: {requirement}" + gemini_fmt
    response = {'message': generate_response(message)}
    print(response)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
