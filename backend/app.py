from flask import Flask, request
from flask_cors import CORS
import query
import os
import logging

app = Flask(__name__)
CORS(app, origins=["https://srrenho.github.io"])

@app.route("/query", methods=["POST"])
def query_api():
    app.logger.info("query recibida")
    data = request.get_json()
    user_input = data.get("user_input", "")
    app.logger.info("user input recibido")
    response = "probando 1 2 3 " #query.generate_response(user_input)
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
