from flask import Flask, request
from flask_cors import CORS
import query
import os

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def query_api():        
    data = request.get_json()
    user_input = data.get("user_input", "")
    response = query.generate_response(user_input)
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
