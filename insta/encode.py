from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt_value(value):
    key = generate_key()
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(value.encode()), key


def decrypt_value(key, value):
    cipher_suite = Fernet(bytes(key))
    return cipher_suite.decrypt(value).decode()