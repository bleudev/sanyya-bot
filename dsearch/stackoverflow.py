from discord import Embed, Colour, ButtonStyle
from discord import ui as UI
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    title = soup.find_all('a', class_='question-hyperlink')[0].get_text()
    post = soup.find_all('div', class_='s-prose js-post-body')[0]
    user_details = soup.find_all('div', class_='user-details')[0]
    quest_time = soup.find_all('div', class_='user-action-time')[0]
    gravatar = soup.find_all('div', class_='user-gravatar32')[0]
    
    text = post.get_text()[:300] + '...'
    user_name = user_details.a.get_text()
    time = quest_time.span.get_text()
    user_avatar_url = gravatar.a.div.img.attrs['src']
    
    footer = f'{user_name} задал этот вопрос {time}'

    emb = Embed(colour=Colour.orange(), title=title, description=text)
    emb.set_footer(text=footer, icon_url=user_avatar_url)
    
    class StackView(UI.View):
        def __init__(self, *, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
    
    return emb, StackView()
