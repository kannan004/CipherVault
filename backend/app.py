from flask import Flask
from services.encryption import encrypt_file, decrypt_file

app = Flask(__name__)

@app.route('/')
def home():
    return '🔐 CipherVault Backend Running'

@app.route('/test')
def test():
    message = b'Hello CipherVault!'
    encrypted = encrypt_file(message)
    decrypted = decrypt_file(encrypted)

    return f'''
    <h2>CipherVault Test</h2>
    <b>Original:</b> {message.decode()}<br><br>
    <b>Encrypted:</b> {encrypted.decode()}<br><br>
    <b>Decrypted:</b> {decrypted.decode()}
    '''

if __name__ == '__main__':
    app.run(debug=True)