import config

def load(filename: str) -> str:
    with open(config.DATA_DIR + filename, "r") as data:
        return data.read()
