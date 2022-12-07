from discord import Embed, Colour, ButtonStyle
from discord import ui as UI
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    title = soup.find_all('a', {'class': "question-hyperlink"})[0].get_text()
    post = soup.find_all('div', {'class': "s-prose js-post-body"})[0]
    
    js_code_blocks = post.find_all('pre', {'class': "lang-js s-code-block"})
    
    for i in js_code_blocks:
        i2 = soup.new_tag('p')
        i2.string = f"""
        ```js
        {i.get_text()}
        ```
        """
        i.replace_with(i2)
    
    text = post.get_text()

    emb = Embed(colour=Colour.orange(), title=title)
    
    emb.add_field(name='None', value=text)
    
    class StackView(UI.View):
        def __init__(self, *, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
    
    return emb, StackView()
