from flask import Flask, request, send_file, jsonify
import os
from aes_crypto import encrypt_file, decrypt_file

app = Flask(__name__)

UPLOAD_FOLDER = "received_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route (required for Render)
@app.route("/")
def home():
    return "Secure File Server Running"

# Upload file
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({"message": "File uploaded", "filename": file.filename})

# Encrypt file
@app.route("/encrypt/<filename>", methods=["GET"])
def encrypt(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    encrypt_file(filepath)
    return jsonify({"message": "File encrypted"})

# Decrypt file
@app.route("/decrypt/<filename>", methods=["GET"])
def decrypt(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    decrypt_file(filepath)
    return jsonify({"message": "File decrypted"})

# Download file
@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_file(filepath, as_attachment=True)

# Render PORT binding
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)