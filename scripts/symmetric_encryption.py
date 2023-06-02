import logging
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logger = logging.getLogger()
logger.setLevel('INFO')


def generate_symmetric_key(key_length: int) -> bytes:
    """
    Функция генерирует ключ симметричного алгоритма шифрования
    :param key_length: Длина ключа
    :return: Ключ
    """
    key = os.urandom(key_length)
    logging.info(f"Ключ симметричного шифрования успешно сгенерирован")
    return key


def symmetric_encryption(key: bytes, text: bytes) -> bytes:
    """
    Функция шифрует текст симметричным алгоритмом шифорвания
    :param key: Ключ шифрования
    :param text: Шифруемый текст
    :return: Зашифрованный текст
    """
    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()
    logging.info("Текст успешно зашифрован")
    return iv + c_text


def symmetric_decryption(key: bytes, text: bytes) -> bytes:
    """
    Функция дешифрует текст симметричным алгоритмом
    :param key: Ключ дешифрования
    :param text: Зашифрованный текст
    :return: Дешифрованный текст
    """
    iv = text[:16]
    text = text[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(text) + decryptor.finalize()
    unpadder = padding.ANSIX923(128).unpadder()
    udc_text = unpadder.update(dc_text) + unpadder.finalize()
    logging.info("Текст успешно расшифрован")
    return udc_text