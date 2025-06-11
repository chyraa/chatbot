import yaml
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Memungkinkan akses dari frontend

# Cek apakah database sudah ada
database_path = "database.db"
database_exists = os.path.exists(database_path)

# Inisialisasi ChatBot
chatbot = ChatBot(
    'SkintoneBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
    ],
    database_uri=f'sqlite:///{database_path}'
)

# Hanya latih chatbot jika database belum ada
if not database_exists:
    print("Melatih chatbot karena database belum ditemukan...")
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")

    with open('training_data/custom_data.yml', 'r') as file:
        data = yaml.safe_load(file)

    custom_trainer = ListTrainer(chatbot)
    for conversation in data['conversations']:
        for i in range(len(conversation) - 1):
            custom_trainer.train([conversation[i], conversation[i + 1]])

# Endpoint API untuk mendapatkan respons chatbot
@app.route('/get_response', methods=['POST'])
def get_response_api():
    user_input = request.json.get('user_input')
    response = chatbot.get_response(user_input)
    return jsonify({'response': str(response)})

# Menjalankan aplikasi Flask dengan Gunicorn untuk Railway
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Gunakan PORT dari Railway
    app.run(debug=False, host="0.0.0.0", port=port)
