from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from database.database import db
from models.user import User


auth = Blueprint("auth", __name__)

bcrypt = Bcrypt()


# -------------------------
# Register API
# -------------------------

@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    if not email or not password:
        return jsonify({
            "message": "Email and Password required"
        }), 400


    existing_user = User.query.filter_by(
        email=email
    ).first()


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



# -------------------------
# Login API
# -------------------------

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


    password_check = bcrypt.check_password_hash(
        user.password,
        password
    )


    if not password_check:
        return jsonify({
            "message": "Invalid email or password"
        }), 401


    token = create_access_token(
    identity=str(user.id)
)


    return jsonify({
        "message": "Login successful",
        "access_token": token
    }), 200



# -------------------------
# Protected Profile API
# -------------------------

@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()


    user = User.query.get(user_id)


    if not user:
        return jsonify({
            "message": "User not found"
        }), 404


    return jsonify({
        "id": user.id,
        "email": user.email
    }), 200