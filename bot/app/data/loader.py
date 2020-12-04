def load(filename: str) -> str:
    with open(filename, "r") as data:
        return data.read()
