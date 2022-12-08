from discord import Embed, Colour, ButtonStyle, Message, PartialEmoji, Interaction
from discord import ui as UI
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    title = soup.find_all('a', class_='question-hyperlink')[0].get_text()
    post = soup.find_all('div', class_='s-prose js-post-body')[0]
    user_details = soup.find_all('div', class_='user-details')[0]
    quest_time = soup.find_all('div', class_='user-action-time')[0]
    gravatar = soup.find_all('div', class_='user-gravatar32')[0]
    
    answers_div = soup.find_all('div', id='answers')[0]
    answers = answers_div.find_all('div', class_='answer js-answer')
    
    text = post.get_text()[:300] + '...'
    
    try:
        user_name = user_details.a.get_text()
    except AttributeError:
        user_name = '*unknown*'

    try:
        time = quest_time.span.get_text()
    except AttributeError:
        time = '*unknown*'
    
    try:
        user_avatar_url = gravatar.a.div.img.attrs['src']
    except AttributeError:
        user_avatar_url = None
    
    footer = f'{user_name} задал этот вопрос {time}'

    emb = Embed(colour=Colour.orange(), title=title, description=text)
    emb.set_footer(text=footer, icon_url=user_avatar_url)
    
    class StackView(UI.View):
        def __init__(self, *, message: Message, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.add_item(UI.Button(style=ButtonStyle.url, url=url, label='Перейти'))
            self.message = message
        
        @UI.button(label='Ответы', custom_id='answers', style=ButtonStyle.green, emoji=PartialEmoji(name='👍'))
        async def answers(self, interaction: Interaction, *args):
            # Ignore 'CommandInvokeError'
            await interaction.response.send_message('Update message!', ephemeral=True)
            await interaction.delete_original_response()

            await self.message.edit(content='Answers', embed=None)
    
    return emb, StackView
