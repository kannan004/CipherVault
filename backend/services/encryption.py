from cryptography.fernet import Fernet
import os


KEY_FILE = "secret.key"


def load_key():

    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

    else:
        with open(KEY_FILE, "rb") as file:
            key = file.read()

    return key



key = load_key()

cipher = Fernet(key)



def encrypt_file(file_data):

    return cipher.encrypt(file_data)



def decrypt_file(encrypted_data):

    return cipher.decrypt(encrypted_data)
