from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from database.database import db
from models.user import User

auth = Blueprint("auth", __name__)

bcrypt = Bcrypt()


@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and Password required"
        }), 400


    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 409


    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")


    user = User(
        email=email,
        password=hashed_password
    )


    db.session.add(user)
    db.session.commit()


    return jsonify({
        "message": "User registered successfully"
    }), 201



@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    user = User.query.filter_by(
        email=email
    ).first()


    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401


    if not bcrypt.check_password_hash(
        user.password,
        password
    ):
        return jsonify({
            "message": "Invalid email or password"
        }), 401


    token = create_access_token(
        identity=user.id
    )


    return jsonify({
        "message": "Login successful",
        "access_token": token
    }), 200