from flask import Flask, request, jsonify
from flask_cors import CORS  # <- Add this import
import openai
import os
import io
import json
app = Flask(__name__)
CORS(app)  # <- Add this to enable CORS for all routes

# Ideally, store this securely using environment variables

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

@app.route('/story', methods=['POST'])
def divide_text():
    data = request.json
    datas = data['ideas']
    divided_text = datas + \
        f"The above sentences are main story that I 'm going to build. Please generate a Json string of one key one value-the key is 'scenes' and the value is the list of {data['number']} number of comic book panel descriptions. Do not include any label or header that indicate the order of the panels. Only the caption descriptions should be a completed paragraph."
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
        scene_content = json.loads(response_message)['scenes']
        return scene_content

    except Exception as e:
        return jsonify({'message': 'Error occurred. Please try again.'}), 500


if __name__ == '__main__':
    app.run(debug=True)