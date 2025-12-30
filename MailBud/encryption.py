from cryptography.fernet import Fernet
from cryptography import exceptions
from dotenv import load_dotenv
import os


class Encryptor():
    load_dotenv("src/certs/credential.env")
    def __init__(self):
        self.key=os.getenv("CIPHER_KEY")
        if self.key is None:
            raise "InvalidKeyError: CIPHER_KEY is None"
        self.fernet_obj=Fernet(self.key)

    def encryptCrutial(self, data: str) -> bytes:
        return self.fernet_obj.encrypt(data.encode()).decode()

    def decryptCrutial(self, data: bytes) -> str:
        return self.fernet_obj.decrypt(data).decode()
