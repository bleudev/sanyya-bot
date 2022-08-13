from api.assistent import main_ass

def main(text: str) -> str:
    def key(key: str):
        return text.lower() == key.lower()

    if key("привет"):
        return "Приветик!"

    if key("как дела?"):
        return "Нормально!"

    if key("хаха"):
        return "Хахахахах"
    
    if key('да'):
        return "Рад, что ты согласен"
    
    if key('нет'):
        return 'Почему нет?'
    
    if len(text) > 100:
        return "Ты решил переписать войну и мир?"

    return main_ass(text)
