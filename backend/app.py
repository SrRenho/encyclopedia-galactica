from flask import Flask, request
from flask_cors import CORS
import query
import database
import os
import threading
import json
from google.cloud import storage

init_done = False

app = Flask(__name__)
CORS(app)

def download_folder_from_gcs(prefix="chroma", local_folder="chroma"):
    print("[GCS] Starting folder download")
    print(f"[GCS] Target local folder: {local_folder}")
    
    print("[GCS] Creating local directory if not exists...")
    os.makedirs(local_folder, exist_ok=True)
    print("[GCS] Directory ready")

    creds = os.environ.get("GCS_CREDENTIALS")
    if creds:
        print("[GCS] Found GCS_CREDENTIALS in environment")
        print("[GCS] Writing credentials to gcloud-creds.json...")
        with open("gcloud-creds.json", "w") as f:
            f.write(creds)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-creds.json"
        print("[GCS] Credential file written and environment variable set")
    else:
        print("[GCS] WARNING: No GCS_CREDENTIALS found in environment")

    print("[GCS] Initializing storage client...")
    client = storage.Client()
    print("[GCS] Client initialized")

    print("[GCS] Getting bucket: encyclopedia-galactica-chromadb")
    bucket = client.bucket("encyclopedia-galactica-chromadb")
    print("[GCS] Listing blobs with prefix:", prefix)
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        print(f"[GCS] Found blob: {blob.name}")
        if blob.name.endswith("/"):
            print(f"[GCS] Skipping folder: {blob.name}")
            continue

        rel_path = blob.name[len(prefix):].lstrip("/")
        local_path = os.path.join(local_folder, rel_path)

        print(f"[GCS] Preparing to download: {blob.name}")
        print(f"[GCS] Local path will be: {local_path}")
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        print(f"[GCS] Downloading to {local_path}...")
        blob.download_to_filename(local_path)
        print(f"[GCS] Downloaded {blob.name} to {local_path}")

    print("[GCS] Folder download complete")


@app.route("/query", methods=["POST"])
def query_api():
    global init_done
    if not init_done:
        return "Server still loading, please try again shortly.", 503
        
    data = request.get_json()
    user_input = data.get("user_input", "")
    response = "probando probando 1 2 3 " #query.generate_response(user_input)
    return response

def init():
    global init_done
    print("descargando database")
    download_folder_from_gcs()
    print("conectando con la IA")
    query.__init__()
    print("Page ready to use!")
    init_done = True

if __name__ == "__main__":
    threading.Thread(target=init, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
