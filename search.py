from requests import get

def search(q: str) -> str:
    url = f"https://www.google.com/search?q={q}"
    data = get(url)
    
    return data
