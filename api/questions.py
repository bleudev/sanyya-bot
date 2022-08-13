from random import choice

def q(text: str):
    text = text.replace("?", "")
    text = text.lower()
    
    if text.startswith("ты"):
        NOT = ["гей", "лох", "пидор", "сука", "дебил", "дура", "дурак", "человек"]
        YES = ["умный", "бот", "хороший"]
        
        q = text.replace("ты", "")
        
        if q in NOT:
            return "Нет"
        if q in YES:
            return "Да"
    else:
        return choice("Нет", "Да")
