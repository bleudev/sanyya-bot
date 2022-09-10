import discord, os
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

bot = discord.Client(intents=discord.Intents.all())
channels = [1008038030042484918, 1008080816166948865]


@bot.event
async def on_ready():
    print("Hi?")


async def textMessage(mes):
    channel = mes.channel
    text_to_be_analyzed = mes.content
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

    DIALOGFLOW_PROJECT_ID = 'small-talk-sanyya-xvlg'
    DIALOGFLOW_LANGUAGE_CODE = 'ru'
    SESSION_ID = 'me'

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
        await mes.reply('Я Вас не совсем понял!')

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id in channels or isinstance(message.channel, discord.DMChannel):
        await textMessage(message)

bot.run("MTAwODAzNjc2NTU5NDAzODM5Mg.GDxyI_.N3egLRxxADvxLku87nUXdA6PojzWIq3ar-V4BI")
