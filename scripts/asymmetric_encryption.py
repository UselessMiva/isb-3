import logging

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger()
logger.setLevel('INFO')


def generate_keys() -> tuple:
    """
    Функция генерирует ключи для асимметричного шифрования
    :return: Функция возвращает пару ключей для асимметричного шифрования
    """
    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = keys
    public_key = keys.public_key()
    logging.info("Ключи асимметричного шифрования успешно созданы")
    return private_key, public_key


def asymmetric_encrypt(public_key, text: bytes) -> bytes:
    """
    Функция шифрует текст с помощью асимметричного алгоритма кодирования
    :param public_key: Публичный ключ
    :param text: Шифруемый текст
    :return: Зашифрованный текст
    """
    c_text = public_key.encrypt(text,
                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                             label=None))
    logging.info("Текст успешно зашифрован")
    return c_text


def asymmetric_decrypt(private_key, text: bytes) -> bytes:
    """
    Функция расшифровывает текст
    :param private_key: Приватный ключ
    :param text: Расшифровываемый текст
    :return: Расшифрованный текст
    """
    dc_text = private_key.decrypt(text,
                                  padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                               label=None))
    logging.info("Текст успешно расшифрован")
    return dc_text


def serialize_asymmetric_keys(public_key, private_key, public_pem: str, private_pem: str) -> None:
    """
    Функция сериализует ключи асимметричного алгоритма шифрования
    :param public_key: Публичный ключ
    :param private_key: Приватный ключ
    :param public_pem: Путь к файлу в который сериализуется публичный ключ
    :param private_pem: Путь к файлу в который сериализуется приватный ключ
    :return: Функция ничего не возвращает
    """
    try:
        with open(public_pem, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo))
            logging.info("Публичный ключ успешно сериализован")
        with open(private_pem, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption()))
            logging.info("Приватный ключ успешно сериализован")
    except OSError as err:
        logging.warning(f"{err} Не удалось сериализовать ключи")


def deserialize_public_key(file: str):
    """
    Функция десериализует публичный ключ
    :param file: Путь к файлу с сериализованным ключем
    :return: Функция возвращает публичный ключ шифрования
    """
    try:
        with open(file, "rb") as f:
            public_bytes = f.read()
            d_public_key = load_pem_public_key(public_bytes)
            logging.info("Ключ успешно десериализован")
    except OSError as err:
        logging.warning(f"{err} Не удалось десериализовать публичный ключ")
    return d_public_key


def deserialize_private_key(file: str):
    """
    Функция десериализует приватный ключ
    :param file: Путь к файлу с сериализованным ключем
    :return: Функция возвращает приватный ключ шифрования
    """
    try:
        with open(file, "rb") as f:
            private_bytes = f.read()
            d_private_key = load_pem_private_key(private_bytes, password=None)
            logging.info("Ключ успешно десериализован")
    except OSError as err:
        logging.warning(f"{err} Не удалось десериализовать ключ")
    return d_private_key