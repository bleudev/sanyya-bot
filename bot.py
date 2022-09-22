import discord, os
from discord import app_commands, ui
from discord import MessageType as mt
from google.cloud import dialogflow_v2 as dialogflow
from time import sleep
from random import randint
from updates import json as update_json

channels = [1008038030042484918, 1008080816166948865]

channels_json = {i: False for i in channels}


# Dialogflow settings
def change_default_key():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

def change_assistent_key():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key_assistent.json'

DIALOGFLOW_PROJECT_ID = 'small-talk-sanyya-xvlg'
DIALOGFLOW_ASSISTENT_PROJECT_ID = 'sanyya-assistent-cqjy'
SESSION_ID =  f"discord_session_{randint(1, 1000000)}"

endl = "\n"
i_dont_understands = {
    "ru": "Я Вас не понял!",
    "en": "I don't inderstand you"
}


def textMessage(s: str, lang="ru") -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=s,
                                            language_code=lang)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    if response.query_result.fulfillment_text:
        return str(response.query_result.fulfillment_text)
    else:
        return i_dont_understands[lang]

async def AssistentMessage(mes: discord.Message, lang="ru"):
    # $u - Обновления
    s = mes.content

    change_assistent_key()

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_ASSISTENT_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=s,
                                            language_code=lang)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    command = str(response.query_result.fulfillment_text)

    change_default_key()
    
    if command == "$u":
        await mes.reply("Вчера я получил обновление. Хочешь посмотреть?")
    elif command == "$u-yes":
        last_update = update_json[0]
        
        embed = discord.Embed(color=discord.Color.purple(), title=last_update["date_str"])
        embed.add_field(name="Список изменений", value=last_update["changelog"])
        await mes.reply(embed=embed)
    else:
        await mes.reply(command)

def getRussianAlphabet() -> list:
    return [i for i in 'ёйцукенгшщзхъфывапролджэячсмитьбю']


class SanyyaBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)
    
    async def setup_hook(self):
        await self.tree.sync()

bot = SanyyaBot()


@bot.tree.command(description="Информация про бота")
async def инфо(interaction: discord.Interaction):
    await interaction.response.send_message("Оффициальный дискорд сервер: https://discord.gg/8QasqE369f", ephemeral=True)


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


@bot.tree.context_menu(name="Получить ответ")
async def get_answer(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(textMessage(message.content), ephemeral=True)

@bot.event
async def on_ready():
    chans = channels
    guilds = []
    
    for i in chans:
        ch: discord.TextChannel = bot.get_channel(i)
        guilds.append(ch.guild)
    
    for guild in guilds:
        member: discord.Member = guild.get_member(bot.user.id)
        await member.edit(nick="Sanyya | [A]")
    
    activity = discord.Activity(name=f"{len(bot.guilds)} серверов с ботом", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity, status="dnd")

    print("Hi?")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id in channels or isinstance(message.channel, discord.DMChannel):
        message_types = (mt.reply, mt.default, mt.thread_starter_message)

        if not message.type in message_types:
            return

        async with message.channel.typing():
            sleep(0.3)

        l = "en"
        
        for i in message.content.lower():
            if i in getRussianAlphabet():
                l = "ru"
                break
        
        chatmode = channels_json[message.channel.id]
        go_to_chat = ["давай поболтаем"]
        end_chat = ["хватит"]
        
        if chatmode is False:
            if message.content.lower() in go_to_chat:
                channels_json[message.channel.id] = True
                await message.reply('Отлично! Если вам надоест, напишите слово "Хватит"')
                member = message.guild.get_member(bot.user.id)
                await member.edit(nick="Sanyya | [C]")
            else:
                await AssistentMessage(message, lang=l)
        elif chatmode is True:
            if message.content.lower() in end_chat:
                channels_json[message.channel.id] = False
                await message.reply('Надоело? Если ещё захотите пообщаться, напишите "Давай поболтаем"')
                member = message.guild.get_member(bot.user.id)
                await member.edit(nick="Sanyya | [A]")
            else:
                await message.reply(textMessage(message.content, lang=l))

bot.run("MTAwODAzNjc2NTU5NDAzODM5Mg.GDxyI_.N3egLRxxADvxLku87nUXdA6PojzWIq3ar-V4BI")
