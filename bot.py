import discord, os
from discord import app_commands, ui
from google.cloud import dialogflow_v2 as dialogflow
from time import sleep

channels = [1008038030042484918, 1008080816166948865]


# Dialogflow settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'small-talk-sanyya-xvlg'
DIALOGFLOW_LANGUAGE_CODE = 'ru'
SESSION_ID = 'SanyyaBotAI'

endl = "\n"


def textMessage(mes) -> str:
    text_to_be_analyzed = mes.content

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed,
                                            language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    if response.query_result.fulfillment_text:
        return str(response.query_result.fulfillment_text)
    else:
        return 'Я Вас не понял!'


class SanyyaBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)
        self.allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
    
    async def setup_hook(self):
        await self.tree.sync()

bot = SanyyaBot()

@bot.tree.command(description="Информация про бота")
async def инфо(interaction: discord.Interaction):
    await interaction.response.send_message("Оффициальный дискорд сервер: https://discord.gg/8QasqE369f")


@bot.tree.command(description="Сообщить о баге")
async def баг(interaction: discord.Interaction):
    class BugReportModal(ui.Modal, title='Сообщить о баге'):
        your_message = ui.TextInput(label="Ваше сообщение",
                               style=discord.TextStyle.paragraph,
                               custom_id="your_message",
                               placeholder="Привет!")

        bot_message = ui.TextInput(label="Ответ бота",
                               style=discord.TextStyle.paragraph,
                               custom_id="bot_message",
                               placeholder="Приветик! Как дела?")
        
        additional_info = ui.TextInput(label="Дополнительная информация",
                                       style=discord.TextStyle.long,
                                       custom_id="additional_info",
                                       placeholder='Должен отвечать "Привет!"',
                                       required=False,
                                       min_length=10)

        profile_for_connection = ui.TextInput(label="Профиль для связи",
                                              style=discord.TextStyle.short,
                                              custom_id="profile_for_connection",
                                              placeholder="name#1234",
                                              required=False,
                                              min_length=5,
                                              max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            channel = bot.get_channel(1018276325703811222)
            
            message = str(self.your_message) + (endl * 2) + str(self.bot_message)

            mes = ""

            if self.profile_for_connection.value:
                mes += "Профиль для связи: " + str(self.profile_for_connection) + (endl * 2)
            
            if self.additional_info.value:
                mes += "Дополнительная информация: " + str(self.additional_info) + (endl * 2)
            
            mes += message
            
            await channel.send(mes)
            
            await interaction.response.send_message('Спасибо!', ephemeral=True)
    
    await interaction.response.send_modal(BugReportModal())


@bot.tree.command(description="Предложить идею")
async def идея(interaction: discord.Interaction):
    class IdeaModal(ui.Modal, title='Предложить идею'):
        your_message = ui.TextInput(label="Ваше сообщение",
                               style=discord.TextStyle.paragraph,
                               custom_id="your_message",
                               placeholder="Привет!")

        bot_message = ui.TextInput(label="Ответ бота",
                               style=discord.TextStyle.paragraph,
                               custom_id="bot_message",
                               placeholder="Приветик! Как дела?")

        profile_for_connection = ui.TextInput(label="Профиль для связи",
                                              style=discord.TextStyle.short,
                                              custom_id="profile_for_connection",
                                              placeholder="name#1234",
                                              required=False,
                                              min_length=5,
                                              max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            channel = bot.get_channel(1018508847750586448)
            
            message = str(self.your_message) + (endl * 2) + str(self.bot_message)

            mes = message

            if self.profile_for_connection.value:
                mes = "Профиль для связи: " + str(self.profile_for_connection) + (endl * 2) + str(message)
            
            await channel.send(mes)
            
            await interaction.response.send_message('Спасибо!', ephemeral=True)
    
    await interaction.response.send_modal(IdeaModal())


@bot.event
async def on_ready():
    print("Hi?")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id in channels or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            sleep(0.3)

        await textMessage(message)

bot.run("MTAwODAzNjc2NTU5NDAzODM5Mg.GDxyI_.N3egLRxxADvxLku87nUXdA6PojzWIq3ar-V4BI")
