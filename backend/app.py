from flask import Flask, request
from flask_cors import CORS
import query
import database
import os
import threading

init_done = False

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def query_api():
    if not init_done:
        return "Server still loading, please try again shortly.", 503
        
    data = request.get_json()
    user_input = data.get("user_input", "")
    response = "probando probando 1 2 3 " #query.generate_response(user_input)
    return response

def init():
    print("creando database")
    database.generate_data_store()
    print("conectando con la IA")
    query.__init__()
    print("Page ready to use!")
    init_done = True

if __name__ == "__main__":
    threading.Thread(target=init, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
