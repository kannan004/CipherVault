from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from config import Config
from database.database import db

from models.user import User
from models.file import File

from routes.auth import auth
from routes.files import files


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)


# Register APIs
app.register_blueprint(auth)
app.register_blueprint(files)


# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "🔐 CipherVault Backend Running"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )                                   