from cryptography.fernet import Fernet
from pathlib import Path


KEY_FILE = Path("secret.key")


def load_or_create_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()

    key = Fernet.generate_key()

    KEY_FILE.write_bytes(key)

    return key


KEY = load_or_create_key()

cipher = Fernet(KEY)


def encrypt_text(text):
    if not text:
        return ""

    encrypted = cipher.encrypt(
        text.encode()
    )

    return encrypted.decode()


def decrypt_text(encrypted_text):
    if not encrypted_text:
        return ""

    decrypted = cipher.decrypt(
        encrypted_text.encode()
    )

    return decrypted.decode()