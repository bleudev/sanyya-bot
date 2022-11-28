from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
from requests import get

def p(*t):
    r = ''
    for i in t:
        r += i
    return r

endl = '\n'
endl2 = endl * 2

def searchh(q: str) -> str:
    url = [i for i in search(q, stop=1, lang='ru', country='russia', pause=0) ][0]
    data = get(url).text
    soup = BeautifulSoup(data)
    
    return p(soup.title.text, endl2, url)
