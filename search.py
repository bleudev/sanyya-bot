from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
from requests import get
from urllib.parse import urlparse
from discord import Embed, ButtonStyle, Colour
from discord import ui as UI
from discord.ui import View
import views
from dsearch import wiki, stackoverflow

def p(*t):
    r = ''
    for i in t:
        r += i
    return r

endl = '\n'
endl2 = endl * 2

supported_urls = [
    'ru.wikipedia.org',
    'ru.stackoverflow.com',
]

def searchh(q: str) -> str:
    if q.startswith('https://'):
        url = q
    else:
        url = [i for i in search(q, stop=1, lang='ru', country='russia', pause=0) ][0]
    
    # Information about page
    parsed = urlparse(url)
    host = parsed.hostname
    data = get(url).text
    soup = BeautifulSoup(data)
    title = soup.title.text

    if host in supported_urls:  # DSearch
        return DSearch(url, soup, host)
    
    # SEO analyze
    meta = soup.find_all('meta')
    descs = []

    for tag in meta:  # Find SEO descriptions
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
            descs.append(tag.attrs['content'])
    
    # Result
    emb = Embed(colour=Colour.purple())
    
    try:
        emb.add_field(name=title, value=descs[0])
    except IndexError:
        emb.add_field(name=title, value='No description')
    
    class UrlView(View):
        def __init__(self, link_url, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=link_url, label='Перейти'))
    
    return emb, UrlView(url)

def DSearch(url, soup: BeautifulSoup, host) -> Embed:
    if host == 'ru.wikipedia.org':
        return wiki.ex(soup, url)
    if host == 'ru.stackoverflow.com':
        return stackoverflow.ex(soup, url)
