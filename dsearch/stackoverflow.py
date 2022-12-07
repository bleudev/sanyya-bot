from discord import Embed, Colour, ButtonStyle
from discord import ui as UI
from bs4 import BeautifulSoup, Tag

def ex(soup: BeautifulSoup, url: str):
    title: Tag = soup.find('a', class_='question-hyperlink')
    post: Tag = soup.find('div', class_='s-prose js-post-body')
    
    text = post.get_text()[:100] + '...'

    emb = Embed(colour=Colour.orange(), title=title.get_text())
    
    emb.add_field(name='None', value=text)
    
    class StackView(UI.View):
        def __init__(self, *, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
    
    return emb, StackView()
