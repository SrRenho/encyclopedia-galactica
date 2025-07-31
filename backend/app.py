from flask import Flask, request
from flask_cors import CORS
import query
import database

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def query_api():
    data = request.get_json()
    user_input = data.get("user_input", "")
    response = query.generate_response(user_input)
    return response

if __name__ == "__main__":
    database.generate_data_store()
    query.__init__()
    app.run(host="0.0.0.0", port=5000, debug=True)



