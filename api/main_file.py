from api.assistent import main_ass
from random import choice

def main(text: str) -> str:
    def key(key: str):
        return text.lower() == key.lower()

    def keys(keys: list):
        l = []

        for i in keys:
            l.append(str(i).lower())

        return text.lower() in l

    if keys(["привет", "прив", "всем прив", "всем привет"]):
        return "Приветик!"
    
    if keys(["здрасте", "драсте", "дарова", "здарова"]):
        return "Дарова!"

    if key("как дела?"):
        return "Нормально!"

    if key("хаха"):
        return "Хахахахах"

    if key('да'):
        return "Рад, что ты согласен"

    if key('нет'):
        return 'Почему нет?'

    if len(text) > 100:
        return choice(["Ты решил переписать войну и мир?", "Интересно."])

    return main_ass(text)
