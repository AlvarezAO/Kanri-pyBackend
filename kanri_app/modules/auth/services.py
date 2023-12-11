import secrets
import string
from bcrypt import gensalt, hashpw, checkpw
import base64


def hash_password(password: str) -> str:
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)
    return base64.b64encode(hashed).decode('utf-8')  # Codifica en base64 para almacenar como string


def verify_password(stored_hash: str, provided_password: str) -> bool:
    stored_hash_bytes = base64.b64decode(stored_hash.encode('utf-8'))  # Decodifica de base64 a bytes
    provided_password_bytes = provided_password.encode('utf-8')
    return checkpw(provided_password_bytes, stored_hash_bytes)


def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password
