import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.database import db
from models.file import File

from services.encryption import encrypt_file


files = Blueprint("files", __name__)


VAULT_FOLDER = "vault"


if not os.path.exists(VAULT_FOLDER):
    os.makedirs(VAULT_FOLDER)



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


    # Save encrypted file
    encrypted_filename = (
        uploaded_file.filename + ".enc"
    )


    encrypted_path = os.path.join(
        VAULT_FOLDER,
        encrypted_filename
    )


    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)



    # Save metadata
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