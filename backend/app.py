from flask import Flask, request, jsonify, send_from_directory
from chatbot import ChatBot
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
chatbot = ChatBot()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('../frontend/assets', path)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = chatbot.get_response(user_message)
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)