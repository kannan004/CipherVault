from flask import Flask
from config import Config
from database.database import db
from models.user import User
from services.encryption import encrypt_file, decrypt_file

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "🔐 CipherVault Backend Running"

@app.route("/test")
def test():
    message = b"Hello CipherVault!"

    encrypted = encrypt_file(message)
    decrypted = decrypt_file(encrypted)

    return f"""
    <h2>CipherVault Test</h2>

    <b>Original:</b><br>
    {message.decode()}<br><br>

    <b>Encrypted:</b><br>
    {encrypted.decode()}<br><br>

    <b>Decrypted:</b><br>
    {decrypted.decode()}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)