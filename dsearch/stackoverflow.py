from discord import Embed, Colour, ButtonStyle
from discord import ui as UI
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    title = soup.find('a', class_='question-hyperlink').get_text()
    post = soup.find('div', class_='s-prose js-post-body')
    user_details = soup.find('div', class_='user-details')
    
    text = post.get_text()[:300] + '...'
    user_name = user_details.a.get_text()

    emb = Embed(colour=Colour.orange(), title=title, description=text)
    emb.set_footer(text=user_name)
    
    class StackView(UI.View):
        def __init__(self, *, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
    
    return emb, StackView()
