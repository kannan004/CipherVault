from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from config import Config
from database.database import db
from routes.auth import auth

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

app.register_blueprint(auth)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "🔐 CipherVault Backend Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)