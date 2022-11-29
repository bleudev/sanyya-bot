from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
from requests import get
from urllib.parse import urlparse
from discord import Embed

def p(*t):
    r = ''
    for i in t:
        r += i
    return r

endl = '\n'
endl2 = endl * 2

supported_urls = [
    'ru.wikipedia.org',
]

def searchh(q: str) -> str:
    url = [i for i in search(q, stop=1, lang='ru', country='russia', pause=0) ][0]
    parsed = urlparse(url)
    host = parsed.hostname

    data = get(url).text
    soup = BeautifulSoup(data)

    if host in supported_urls:
        return DSearch(url, soup, host)
    return p(soup.title.text, endl2, url, endl, host)

def DSearch(url, soup: BeautifulSoup, host) -> Embed:
    if host == 'ru.wikipedia.org':
        emb = Embed()
        info = soup.body.p.get_text()
        
        def replace_for(string, format):
            r: str = string
            for i in range(50):
                r = r.replace(format % i, '')
            return r
        
        info = replace_for(info, '[%d]')
        
        info = info.replace('[1]', '').replace('[2]', '').replace('[3]', '').replace('[4]', '').replace('[5]', '')
        emb.add_field(name=soup.title.text, value=info)
        emb.set_footer(text='Powered by Google | DSearch + Sanyya')
        return emb
