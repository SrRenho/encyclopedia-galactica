from flask import Flask, request
from flask_cors import CORS
import query
import os
import logging

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def query_api():
    app.logger.info("query recibida")
    data = request.get_json()
    user_input = data.get("user_input", "")
    app.logger.info("user input recibido")
    response = query.generate_response(user_input, app)
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
