from assistent import main_ass

def main(text: str) -> str:
    def key(key: str):
        return text.lower() == key.lower()

    if key("привет"):
        return "Приветик!"

    if key("как дела?"):
        return "Нормально!"

    if key("хаха"):
        return "Хахахахах"

    return main_ass(text)
