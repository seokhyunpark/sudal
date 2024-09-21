import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)


def generate_response(input_message):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(input_message)
    return response.text


if __name__ == '__main__':
    print(generate_response("Say Hello World."))
