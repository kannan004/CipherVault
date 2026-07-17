import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.database import db
from models.file import File


files = Blueprint("files", __name__)


UPLOAD_FOLDER = "uploads"


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



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



    path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.filename
    )


    uploaded_file.save(path)



    file_record = File(
        filename=uploaded_file.filename,
        filepath=path,
        uploaded_by=user_id
    )


    db.session.add(file_record)
    db.session.commit()



    return jsonify({
        "message": "File uploaded successfully",
        "filename": uploaded_file.filename
    }), 201
