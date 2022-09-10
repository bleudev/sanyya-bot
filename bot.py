import discord, os
from discord import app_commands
from discord.ext import commands
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from time import sleep

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="/")
bot.remove_command('help')

bot.allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)

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


class SanyyaBot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command()
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message("Оффициальный дискорд сервер: https://discord.gg/8QasqE369f")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hi?")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id in channels or isinstance(message.channel, discord.DMChannel):
            async with message.channel.typing():
                sleep(0.3)

            await textMessage(message)

def setup(bot):
    bot.add_cog(SanyyaBot(bot))

setup(bot)

bot.run("MTAwODAzNjc2NTU5NDAzODM5Mg.GDxyI_.N3egLRxxADvxLku87nUXdA6PojzWIq3ar-V4BI")
