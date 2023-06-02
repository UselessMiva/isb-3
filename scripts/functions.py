import logging

logger = logging.getLogger()
logger.setLevel('INFO')


def save_text(text: bytes, file: str) -> None:
    """
    Функция сохраняет текст в файл
    :param text: текст
    :param file: Путь к файлу в который сохраняется текст
    :return: Функция ничего не возвращает
    """
    try:
        with open(file, "wb") as f:
            f.write(text)
            logging.info("Текст успешно сохранен")
    except OSError as err:
        logging.warning(f"{err} Не удалось сохранить текст")


def read_text(file: str) -> bytes:
    """
    Функция считывает текст из файла
    :param file: Путь к файлу
    :return: текст из файла
    """
    try:
        with open(file, 'rb') as f:
            text = f.read()
            logging.info("Текст успешно считан")
    except OSError as err:
        logging.warning(f"{err} Не удалось считать текст")
    return text