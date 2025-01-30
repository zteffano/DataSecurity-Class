# main.py - Just so satisfy the case specification

from caesar import Caesar
from vigenere import Vigenere


def caesarE(key: int, cleartext: str) -> str:
    """Caesar cipher encryption"""
    if not isinstance(key, int) or key <= 0:
        raise ValueError("Key must be a positive integer")
    if not cleartext or not isinstance(cleartext, str):
        raise ValueError("Cleartext must be a non-empty string")

    cipher = Caesar(cleartext)
    return cipher.encrypt(key)


def caesarD(key: int, ciphertext: str) -> str:
    """Caesar cipher decryption"""
    if not isinstance(key, int) or key <= 0:
        raise ValueError("Key must be a positive integer")
    if not ciphertext or not isinstance(ciphertext, str):
        raise ValueError("Ciphertext must be a non-empty string")

    cipher = Caesar(ciphertext)
    return cipher.decrypt(key)


def vigE(key: str, cleartext: str) -> str:
    """Vigenère cipher encryption"""
    if not key or not isinstance(key, str):
        raise ValueError("Key must be a non-empty string")
    if not cleartext or not isinstance(cleartext, str):
        raise ValueError("Cleartext must be a non-empty string")

    cipher = Vigenere(cleartext)
    return cipher.encrypt(key)


def vigD(key: str, ciphertext: str) -> str:
    """Vigenère cipher decryption"""
    if not key or not isinstance(key, str):
        raise ValueError("Key must be a non-empty string")
    if not ciphertext or not isinstance(ciphertext, str):
        raise ValueError("Ciphertext must be a non-empty string")

    cipher = Vigenere(ciphertext)
    return cipher.decrypt(key)
