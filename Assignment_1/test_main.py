# very simple tests for the wrap up in main.py

import pytest
from main import caesarE, caesarD, vigE, vigD


def test_caesar_encryption():
    assert caesarE(7, "Hej med dig, mit navn er anders og jeg kan godt lide kaffe.") == "olq tlk kpn, tpa uhcu ly huklyz vn qln rhu nvka spkl rhmml."
    assert caesarE(1, "xyz") == "yza"


def test_caesar_decryption():
    assert caesarD(3, "khoor") == "hello"
    assert caesarD(1, "yza") == "xyz"


def test_caesar_encryption_decryption():
    text = "test message"
    key = 5
    encrypted = caesarE(key, text)
    decrypted = caesarD(key, encrypted)
    assert decrypted == text


def test_caesar_invalid_inputs():
    with pytest.raises(ValueError):
        caesarE(0, "test")  # Invalid key
    with pytest.raises(ValueError):
        caesarE(1, "")  # Empty string
    with pytest.raises(ValueError):
        caesarE("abc", "test")  # Invalid key type


def test_vigenere_encryption():
    assert vigE("ABC", "The quick brown fox jumps over 13 lazy dogs.") == "tig qvkcl drpyn gqx kwmqu owgr 13 mczz fohu."
    assert vigE("DUH", "THEY DRINK THE TEA") == "wblb xylhr wbl wyh"
    assert vigE("DUH", "they drink the tea") == "wblb xylhr wbl wyh" # ignore casing


def test_vigenere_decryption():
    assert vigD("ABC", "tig qvkcl drpyn gqx kwmqu owgr 13 mczz fohu.") == "the quick brown fox jumps over 13 lazy dogs."
    


def test_vigenere_encryption_decryption():
    text = "test message"
    key = "secret"
    encrypted = vigE(key, text)
    decrypted = vigD(key, encrypted)
    assert decrypted == text


def test_vigenere_invalid_inputs():
    with pytest.raises(ValueError):
        vigE("", "test")  # Empty key
    with pytest.raises(ValueError):
        vigE("key", "")  # Empty text
    with pytest.raises(ValueError):
        vigE(123, "test")  # Invalid key type
