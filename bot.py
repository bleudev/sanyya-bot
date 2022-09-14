import discord, os
from discord import app_commands, ui
from google.cloud import dialogflow_v2 as dialogflow
from time import sleep
import asqlite

channels = [1008038030042484918, 1008080816166948865]


# Dialogflow settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'small-talk-sanyya-xvlg'
SESSION_ID = 'SanyyaBotAI'

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

def AssistentMessage(s: str, lang="ru") -> str:
    # $u - Обновления

    raw = ""
    
    for i in s.lower():
        if not i in [".", ",", "?", "!"]:
            raw += i
    
    commands = [
        (["что в тебе обновилось", "обновления"], "$u")
    ]
    
    command = ""

    for texts, com in commands:
        if raw in texts:
            command = com
            break
    
    if command == "$u":
        return "Вчера я получил обновление. Хочешь посмотреть?"
    else:
        return "Неизвестная команда"

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


async def update_db() -> None:
    async with asqlite.connect('channels.db') as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("SELECT * FROM channels")

                rows = await cursor.fetchall()
                
                global channels
                channels = [ch["id"] for ch in rows]
                
                activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(channels)} каналов с ботом")
                await bot.change_presence(activity=activity, status="dnd")
            except:
                pass


@bot.tree.command(description="Привязать бота к этому каналу")
async def привязать(interaction: discord.Interaction):
    channel_id = interaction.channel_id

    async with asqlite.connect('channels.db') as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute('''CREATE TABLE channels
                                        (id text,chatmode bit)''')
            except:
                pass
            
            await cursor.execute(f"INSERT INTO channels VALUES ('{str(channel_id)}',0)")

            await conn.commit()
    
    await update_db()
    await interaction.response.send_message("Готово!", ephemeral=True)


@bot.tree.command(description="Отвязать бота от этого канала")
async def отвязать(interaction: discord.Interaction):
    channel_id = interaction.channel_id

    async with asqlite.connect('channels.db') as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute('''CREATE TABLE channels
                                        (id text,chatmode bit)''')
            except:
                pass
            
            try:
                await cursor.execute(f"DELETE from channels where id = {str(channel_id)}")
                
                await conn.commit()
            except:
                await update_db()

                await interaction.response.send_message("Этот канал не привязан к боту", ephemeral=True)
                return
    
    await update_db()
    await interaction.response.send_message("Готово!", ephemeral=True)


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
    await update_db()
    print("Hi?")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if str(message.channel.id) in channels or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            sleep(0.3)

        l = "en"
        
        for i in message.content.lower():
            if i in getRussianAlphabet():
                l = "ru"
                break
        
        async with asqlite.connect('channels.db') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SELECT chatmode FROM channels WHERE id = '{message.channel.id}'")

                row = await cursor.fetchone()
                chatmode = row["chatmode"]
                
                go_to_chat = ['давай поболтаем']
                end_chat = ['хватит']
                
                if chatmode == 0:
                    if message.content.lower() in go_to_chat:
                        await cursor.execute(f"UPDATE channels SET chatmode = 1 WHERE id = '{message.channel.id}'")
                        await message.reply('Отлично! Если вам надоест, напишите слово "Хватит"')
                    else:
                        await message.reply(AssistentMessage(message.content, lang=l))
                elif chatmode == 1:
                    if message.content.lower() in end_chat:
                        await cursor.execute(f"UPDATE channels SET chatmode = 0 WHERE id = '{message.channel.id}'")
                        await message.reply('Надоело? Если ещё захотите пообщаться, напишите "Давай поболтаем"')
                    else:
                        await message.reply(textMessage(message.content, lang=l))

bot.run("MTAwODAzNjc2NTU5NDAzODM5Mg.GDxyI_.N3egLRxxADvxLku87nUXdA6PojzWIq3ar-V4BI")
