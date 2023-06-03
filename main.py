import argparse

from scripts.symmetric_encryption import generate_symmetric_key, symmetric_decryption, symmetric_encryption
from scripts.functions import read_text, save_text
from scripts.asymmetric_encryption import generate_keys, asymmetric_decrypt, asymmetric_encrypt, serialize_asymmetric_keys, deserialize_private_key
from scripts.settings import read_settings


def generation():
    symmetric_key = generate_symmetric_key(settings['key_length'])
    private_key, public_key = generate_keys()
    serialize_asymmetric_keys(public_key, private_key, settings['public_key'], settings['private_key'])
    save_text(asymmetric_encrypt(public_key, symmetric_key), settings['symmetric_key'])


def encryption():
    private_key = deserialize_private_key(settings['private_key'])
    c_key = read_text(settings['symmetric_key'])
    symmetric_key = asymmetric_decrypt(private_key, c_key)
    text = read_text(settings['initial_file'])
    c_text = symmetric_encryption(symmetric_key, text)
    save_text(c_text, settings['encrypted_text'])


def decryption():
    private_key = deserialize_private_key(settings['private_key'])
    c_key = read_text(settings['symmetric_key'])
    symmetric_key = asymmetric_decrypt(private_key, c_key)
    c_text = read_text(settings['encrypted_text'])
    text = symmetric_decryption(symmetric_key, c_text)
    save_text(text, settings['decrypted_text'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cus', '--custom', type=str,
                        help='Использует пользовательский файл с настройками, необходимо указать путь к файлу')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action="store_true", help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action="store_true", help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', action="store_true", help='Запускает режим дешифрования')
    args = parser.parse_args()
    if args.custom:
        settings = read_settings(args.custom)
    else:
        settings = read_settings()
    if settings:
        if args.generation:
            generation()
        elif args.encryption:
            encryption()
        else:
            decryption()