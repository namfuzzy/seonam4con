import base64
import os
from typing import Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _derive_key(secret: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend(),
    )
    return kdf.derive(secret.encode("utf-8"))


def encrypt(secret: str, plaintext: str) -> str:
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = _derive_key(secret, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    payload = base64.urlsafe_b64encode(salt + iv + ciphertext).decode("utf-8")
    return payload


def decrypt(secret: str, payload: str) -> str:
    raw = base64.urlsafe_b64decode(payload)
    salt = raw[:16]
    iv = raw[16:32]
    ciphertext = raw[32:]
    key = _derive_key(secret, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")


def mask_value(value: str, visible: int = 4) -> str:
    if len(value) <= visible:
        return value
    hidden = "*" * (len(value) - visible)
    return f"{hidden}{value[-visible:]}"
