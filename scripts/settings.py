import logging
import json

logger = logging.getLogger()
logger.setLevel('INFO')

settings = {
    'initial_file': 'files/initial_file.txt',
    'encrypted_text': 'files/encrypted_text.txt',
    'decrypted_text': 'files/decrypted_text.txt',
    'symmetric_key': 'files/symmetric_key.txt',
    'public_key': 'files/public_key.pem',
    'private_key': 'files/private_key.pem',
    'key_length': 16
}


def read_settings(file_with_settings: str = "files/settings.json") -> dict:
    """
    Функция считывает настройки из файла
    :param file_with_settings: Путь к файлу с настройками
    :return: Настройки
    """
    settings = None
    try:
        with open(file_with_settings, "r") as f:
            settings = json.load(f)
        logging.info("Настройки успешно считаны")
    except OSError as err:
        logging.warning(f"{err} Не удалось считать настройки")
    return settings


if __name__ == "__main__":
    with open('../files/settings.json', "w") as f:
        json.dump(settings, f)