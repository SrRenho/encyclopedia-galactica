from flask import Flask, request
from flask_cors import CORS
import query
import database
import os
import threading
import json
from google.cloud import storage

def download_folder_from_gcs(prefix="chroma", local_folder="chroma"):
    os.makedirs(local_folder, exist_ok=True)

    # Write credentials to a temp file
    creds = os.environ.get("GCS_CREDENTIALS")
    if creds:
        with open("gcloud-creds.json", "w") as f:
            f.write(creds)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-creds.json"

    client = storage.Client()
    bucket = client.bucket("encyclopedia-galactica-chromadb")
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        if blob.name.endswith("/"):  # Skip folders
            continue
        rel_path = blob.name[len(prefix):].lstrip("/")
        local_path = os.path.join(local_folder, rel_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        blob.download_to_filename(local_path)
        print(f"Downloaded {blob.name} to {local_path}")


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
    print("descargando database")
    download_folder_from_gcs()
    print("conectando con la IA")
    query.__init__()
    print("Page ready to use!")
    init_done = True

if __name__ == "__main__":
    threading.Thread(target=init, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
