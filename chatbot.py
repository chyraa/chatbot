import yaml
from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os

# Membuat instance Flask
app = Flask(__name__)

# Membuat instance chatbot
chatbot = ChatBot(
    'SkintoneBot', 
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
    ],
    database_uri='sqlite:///database.db'
)

# Fungsi untuk melatih chatbot dengan custom data dari custom_data.yml
def train_custom_data():
    with open('training_data/custom_data.yml', 'r') as file:
        data = yaml.safe_load(file)

    trainer = ListTrainer(chatbot)
    
    for conversation in data['conversations']:
        for i in range(0, len(conversation), 2):
            question = conversation[i]
            answer = conversation[i + 1]
            trainer.train([question, answer])

# Menentukan pelatihan untuk chatbot menggunakan ChatterBot Corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Melatih chatbot dengan data custom
train_custom_data()

# Endpoint API untuk mendapatkan respons chatbot
@app.route('/get_response', methods=['POST'])
def get_response_api():
    user_input = request.json.get('user_input')
    response = chatbot.get_response(user_input)
    return jsonify({'response': str(response)})

# Fungsi tambahan agar `get_response()` bisa dipanggil langsung dari `app.py`
def get_response(user_input):
    response = chatbot.get_response(user_input)
    return str(response)

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway menentukan port sendiri
    app.run(debug=False, host="0.0.0.0", port=port)
    
