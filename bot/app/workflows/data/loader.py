import config

def load(filename: str) -> str:
    # возвращает содержимое файлов из папки data
    with open(config.DATA_DIR + filename, "r") as data:
        return data.read()
