from Crypto.Cipher import AES
import os

KEY = b'1234567890123456'  # 16-byte key

def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt_file(filepath):
    cipher = AES.new(KEY, AES.MODE_ECB)

    with open(filepath, "rb") as f:
        data = f.read()

    encrypted = cipher.encrypt(pad(data))

    with open(filepath, "wb") as f:
        f.write(encrypted)

def decrypt_file(filepath):
    cipher = AES.new(KEY, AES.MODE_ECB)

    with open(filepath, "rb") as f:
        data = f.read()

    decrypted = cipher.decrypt(data).rstrip(b" ")

    with open(filepath, "wb") as f:
        f.write(decrypted)
