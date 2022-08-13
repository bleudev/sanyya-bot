from .vars import INFO

def main_ass(text: str):
    def key(key: str):
        return text.lower() == key.lower()

    if key("инфо"):
        return INFO
