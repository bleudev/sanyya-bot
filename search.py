from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
from requests import get

def searchh(q: str) -> str:
    url = [i for i in search(q, stop=1, lang='ru') ][0]
    data = get(url).text
    soup = BeautifulSoup(data)
    
    return soup.title.text
