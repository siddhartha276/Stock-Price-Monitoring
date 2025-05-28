from flask import Flask, jsonify, request
from flask_cors import CORS
from ChatBot.chat_models import ChatBot

app = Flask(__name__)
CORS(app)

bot = ChatBot()

@app.route('/generateResponse', methods=['POST'])
def get_query():
    data = request.get_json()
    user_query = data.get('query', '')

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        response_list = bot.generate_response(user_query)
        final_response = " ".join(response_list)
        print(final_response)
        return jsonify({"response": final_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
