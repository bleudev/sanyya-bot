from discord import Embed, Colour, ButtonStyle
from discord import ui as UI
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    title = soup.find_all('a', {'class': "question-hyperlink"})[0].get_text()
    post = soup.find_all('a', {'div': "postcell post-layout--right"})[0].get_text()
    emb = Embed(colour=Colour.orange(), title=title)
    
    emb.add_field(name='None', value=post)
    
    class StackView(UI.View):
        def __init__(self, *, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
    
    return emb, StackView()
