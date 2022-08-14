from random import choice

def q(text: str):
    text = text.replace("?", "")
    text = text.lower()
    
    def key(key: str):
        return text == key.lower()
    
    if key("как дела"):
        return "Нормально!"
    
    NOT = ["гей", "лох", "пидор", "сука", "дебил", "дура", "дурак", "человек"]
    YES = ["умный", "бот", "хороший"]
        
    if text in NOT:
        return "Нет"
    if text in YES:
        return "Да"
    return choice(["Нет", "Да"])
