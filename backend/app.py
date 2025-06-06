from flask import Flask, request, jsonify
from chatbot import ChatBot
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
chatbot = ChatBot()

# Train the chatbot with some basic knowledge
chatbot.train([
    ("Como instalo um programa", "Para instalar um programa, vá em Configurações > Aplicativos > Adicionar novo programa."),
    ("Preciso de ajuda com login", "Você pode redefinir sua senha na página de login clicando em 'Esqueci minha senha'."),
    ("Onde encontro configurações", "As configurações estão no canto superior direito, clique no ícone de engrenagem."),
    ("sair", "Até logo! Espero ter ajudado."),
    ("quero sair", "Até mais! Volte sempre que precisar."),
    ("encerrar", "Encerrando a sessão. Tenha um bom dia!")
])

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)