from cryptography.fernet import Fernet
import os

# File where the encryption key will be stored
KEY_FILE = "secret.key"


def generate_key():
    """Generate a new encryption key if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_key():
    """Load the encryption key from the key file."""
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


# Generate the key if it doesn't exist
generate_key()

# Load the key
key = load_key()

# Create a Fernet object
fernet = Fernet(key)


def encrypt_file(file_data):
    """
    Encrypt file data.

    Args:
        file_data (bytes): Original file content.

    Returns:
        bytes: Encrypted file content.
    """
    return fernet.encrypt(file_data)


def decrypt_file(file_data):
    """
    Decrypt encrypted file data.

    Args:
        file_data (bytes): Encrypted file content.

    Returns:
        bytes: Original file content.
    """
    return fernet.decrypt(file_data)