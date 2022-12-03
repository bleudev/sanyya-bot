from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
from requests import get
from urllib.parse import urlparse
from discord import Embed, ButtonStyle
from discord import ui as UI
from discord.ui import View
import views

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
    emb = Embed()
    emb.add_field(name=title, value=descs[0])
    
    class UrlView(View):
        def __init__(self, *, link_url, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=link_url, label='Перейти'))
    
    return emb, UrlView(url)

def DSearch(url, soup: BeautifulSoup, host) -> Embed:
    if host == 'ru.wikipedia.org':
        emb = Embed()
        ipa = soup.find_all('span', {'class': 'IPA'})[0]
        ipa.decompose()
        info = soup.body.p.get_text()
        
        def replace_for(string, format):
            r: str = string
            for i in range(50):
                r = r.replace(format % i, '')
            return r
        
        info = replace_for(info, '[%d]')
        
        info = info.replace('[1]', '').replace('[2]', '').replace('[3]', '').replace('[4]', '').replace('[5]', '')
        title = soup.title.text + '  ' + views.emoji.beta
        
        emb.add_field(name=title, value=info)
        emb.set_footer(text='Powered by Google | DSearch + Sanyya')
        
        class WikiView(View):
            def __init__(self, *, timeout: float = 180):
                super().__init__(timeout=timeout)
                self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
        
        return emb, WikiView()
