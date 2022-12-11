from discord import Embed, Colour, ButtonStyle, Message, Interaction
from discord import ui as UI
from bs4 import BeautifulSoup

def ex(soup: BeautifulSoup, url: str):
    title = soup.find_all('a', class_='question-hyperlink')[0].get_text()
    post = soup.find_all('div', class_='s-prose js-post-body')[0]
    user_details = soup.find_all('div', class_='user-details')[0]
    quest_time = soup.find_all('div', class_='user-action-time')[0]
    gravatar = soup.find_all('div', class_='user-gravatar32')[0]
    
    answers_div = soup.find_all('div', id='answers')[0]
    accepted_answers = answers_div.find_all('div', class_='answer js-answer accepted-answer js-accepted-answer')
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
        
        @UI.button(label='Вопрос', custom_id='question', style=ButtonStyle.grey)
        async def question(self, interaction: Interaction, *a, **k):
            emb, view = ex(soup, url)
            view = view(message=self.message)

            await self.message.edit(embed=emb, view=view, content='')
            await interaction.response.defer() # Ignore errors
        
        @UI.button(label='Ответы', custom_id='answers', style=ButtonStyle.green)
        async def answers(self, interaction: Interaction, *a, **k):
            emb = Embed(colour=Colour.orange(), title='Ответы')
            
            if accepted_answers != []:
                answ = accepted_answers[0]
                layout = answ.find_all('div', class_='post-layout')[0]
                answercell_layout = layout.find_all('div', class_='answercell post-layout--right')[0]
                answer_body = answercell_layout.find_all('div', class_='s-prose js-post-body')[0]
                text = answer_body.get_text()[:300] + '...'
                
                emb.add_field(name='Лучший ответ ✅', value=text)
            
            await self.message.edit(content='Answers', embed=None)
            await interaction.response.defer() # Ignore errors
    
    return emb, StackView
