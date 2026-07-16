from flask import Flask
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to File Encrypter API!"


@app.route("/test")
def test():
    message = b"Hello Kannan!"

    encrypted = encrypt_file(message)
    decrypted = decrypt_file(encrypted)

    return f"""
    <h2>File Encrypter Test</h2>

    <b>Original Message:</b><br>
    {message.decode()}<br><br>

    <b>Encrypted Message:</b><br>
    {encrypted.decode()}<br><br>

    <b>Decrypted Message:</b><br>
    {decrypted.decode()}
    """


if __name__ == "__main__":
    app.run(debug=True)