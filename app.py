from flask import Flask
from flask import render_template
from gemini import generate_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sudal.html')


if __name__ == '__main__':
    app.run(debug=True)
