import os

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.database import db
from models.file import File

from services.encryption import encrypt_file, decrypt_file


files = Blueprint("files", __name__)


VAULT_FOLDER = "vault"
UPLOAD_FOLDER = "uploads"


os.makedirs(VAULT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# -------------------------
# Upload + Encryption API
# -------------------------

@files.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():

    user_id = get_jwt_identity()


    if "file" not in request.files:
        return jsonify({
            "message": "No file provided"
        }), 400


    uploaded_file = request.files["file"]


    if uploaded_file.filename == "":
        return jsonify({
            "message": "Filename missing"
        }), 400



    # Read original file
    file_data = uploaded_file.read()


    # Encrypt file
    encrypted_data = encrypt_file(
        file_data
    )


    # Store encrypted file
    encrypted_filename = (
        uploaded_file.filename + ".enc"
    )


    encrypted_path = os.path.join(
        VAULT_FOLDER,
        encrypted_filename
    )


    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)



    # Save file information
    file_record = File(
        filename=uploaded_file.filename,
        filepath=encrypted_path,
        uploaded_by=user_id
    )


    db.session.add(file_record)
    db.session.commit()


    return jsonify({
        "message": "File encrypted and uploaded successfully",
        "filename": uploaded_file.filename
    }), 201




# -------------------------
# Download + Decryption API
# -------------------------

@files.route("/download/<filename>", methods=["GET"])
@jwt_required()
def download_file(filename):


    encrypted_path = os.path.join(
        VAULT_FOLDER,
        filename + ".enc"
    )


    if not os.path.exists(encrypted_path):
        return jsonify({
            "message": "File not found"
        }), 404



    # Read encrypted file
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()



    # Decrypt file
    decrypted_data = decrypt_file(
        encrypted_data
    )



    # Temporary decrypted file
    decrypted_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)



    return send_file(
        decrypted_path,
        as_attachment=True
    )