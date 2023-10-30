from flask import Flask, request, jsonify
from flask_cors import CORS  # <- Add this import
import openai
import json
import os
import io
app = Flask(__name__)
CORS(app)  # <- Add this to enable CORS for all routes

# Ideally, store this securely using environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
def format_story(input_string):
    sentences = input_string.split("#")
    formatted_story = ""
    
    for index, sentence in enumerate(sentences):
        if sentence:  # Check if the sentence is not empty
            formatted_story += f"Scene {index + 1} {sentence.strip()} "

    return formatted_story.strip()

@app.route('/story', methods=['POST'])
def divide_text():
    data = request.json
    datas = data['ideas']
    divided_text = format_story(datas) + \
        f"Please generate a Json string of one key one value-The key is 'scenes' and the value is the list of scene description but the character 's name will be replaced by one famous celebrities full name."
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": divided_text}
            ]
        )
        response_message = response.choices[0].message['content']
        return response_message

    except Exception as e:
        return jsonify({'message': 'Error occurred. Please try again.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
