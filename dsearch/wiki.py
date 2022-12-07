from discord import Embed, Colour, ButtonStyle
from discord import ui as UI
import views
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    emb = Embed(colour=Colour.from_rgb(255, 255, 255))
    ipa = soup.find_all('span', {'class': 'IPA'})[0]
    ipa.decompose()
    info = soup.body.p.get_text()
    
    def replace_for(string, formt):
        r: str = string
        for i in range(50):
            r = r.replace(formt % i, '')
        return r
    
    info = replace_for(info, '[%d]')
    
    info = info.replace('[1]', '').replace('[2]', '').replace('[3]', '').replace('[4]', '').replace('[5]', '')
    title = soup.title.text + '  ' + views.emoji.beta
    
    emb.add_field(name=title, value=info)
    emb.set_footer(text='Powered by Google | DSearch + Sanyya')
    
    class WikiView(UI.View):
        def __init__(self, *, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
    
    return emb, WikiView()
