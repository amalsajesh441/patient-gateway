from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_value(value: str) -> str:
    if not value:
        return None
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str:
    if not value:
        return None
    return fernet.decrypt(value.encode()).decode()
