import discord, os
from discord import app_commands, ui
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from time import sleep

channels = [1008038030042484918, 1008080816166948865]


# Dialogflow settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'small-talk-sanyya-xvlg'
DIALOGFLOW_LANGUAGE_CODE = 'ru'
SESSION_ID = 'SanyyaBotAI'


async def textMessage(mes):
    text_to_be_analyzed = mes.content

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    if response.query_result.fulfillment_text:
        await mes.reply(str(response.query_result.fulfillment_text))
    else:
        await mes.reply('Я Вас не понял!')


class SanyyaBot(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        await self.tree.sync()

bot = SanyyaBot(intents=discord.Intents.all())

bot.allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)

@bot.tree.command(description="Информация про бота")
async def инфо(interaction: discord.Interaction):
    await interaction.response.send_message("Оффициальный дискорд сервер: https://discord.gg/8QasqE369f")


@bot.tree.command(description="Сообщить о баге")
async def баг(interaction: discord.Interaction):
    class BugReportModal(ui.Modal, title='Сообщить о баге'):
        message = ui.TextInput(label="Сообщение",
                               style=discord.TextStyle.long,
                               custom_id="bug_report",
                               placeholder="Не работает команда /инфо")

        profile_for_connection = ui.TextInput(label="Профиль для связи",
                                              style=discord.TextStyle.short,
                                              custom_id="profile_for_connection",
                                              placeholder="name#1234",
                                              required=False,
                                              min_length=5,
                                              max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            channel = bot.get_channel(1018276325703811222)
            
            mes = self.message
            
            if self.profile_for_connection.value:
                mes = "Профиль для связи: " + str(self.profile_for_connection) + "\n\n" + str(self.message)
            
            await channel.send(mes)
            
            await interaction.response.send_message('Спасибо!', ephemeral=True)
    
    await interaction.response.send_modal(BugReportModal())

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
