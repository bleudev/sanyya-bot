import discord, os
from discord import app_commands, ui, Embed, Colour
from discord.ext.tasks import loop
from discord import MessageType as mt

from google.api_core.protobuf_helpers import get_messages
from google.cloud import dialogflow_v2 as dialogflow

from time import sleep
from random import randint
from datetime import datetime
from pytz import timezone

from updates import json as update_json
from search import searchh

channels = [1045559879772934215, 1046835447592136775]

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


def textMessage(s: str) -> str:
    change_default_key()
    
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=s,
                                            language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    if response.query_result.fulfillment_text:
        return str(response.query_result.fulfillment_text)
    else:
        return 'Что ты сказал?'

async def get_update_by_its_id(uid: int, message: discord.Message):
    upd = update_json[uid]
    date = upd["date"]
    name = upd["name"]
    changelog = ''
    with open(f'changelog/{name}', 'r', encoding='utf-8') as f:
        changelog = f.read()

    embed = discord.Embed(color=discord.Color.purple(), title=name)
    embed.add_field(name="Список изменений", value=changelog)
    await message.reply(embed=embed)

async def AssistentMessage(mes: discord.Message):
    # $u - Обновления
    # $t - Время
    # $hex - Посмотреть цвет
    s = mes.content

    change_assistent_key()

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_ASSISTENT_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=s,
                                            language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    command = str(response.query_result.fulfillment_text)

    change_default_key()
    
    if command == "u":
        last_update = update_json[0]
        update_date = last_update["date"].toordinal()
        now_date = datetime.now(timezone('Europe/Moscow')).date().toordinal()
        days_ago = now_date - update_date
        
        data_day_strs = [
            ("Сегодня", 0),
            ("Вчера", 1),
            ("Позавчера", 2),
            ("Месяц назад", 30)
        ]
        
        _day_str = ""
        
        for day_str, ago in data_day_strs[::-1]:
            if days_ago >= ago:
                _day_str = day_str
                break
        
        await mes.reply(f"{_day_str} я получил обновление. Хочешь посмотреть?")
    elif command == "u-yes":
        await get_update_by_its_id(0, mes)
    elif command == "u-no":
        await mes.reply("Ну, как хочешь")
    elif command == "u2":
        await get_update_by_its_id(1, mes)
    elif command.startswith("t"):
        city = command.replace('t ', '')
        city = city.replace(' ', '')
        
        cities = {
            'Москва': 'Europe/Moscow',
            'Киев': 'Europe/Kiev',
            'Калининград': 'Europe/Kaliningrad',
            'Лондон': 'Europe/London',
            'Минск': 'Europe/Minsk',
            'Владивосток': 'Asia/Vladivostok'
        }

        tzs = ''
        
        for i in cities.keys():
            tzs += (i + ', ')

        tz = timezone(cities[city])
        
        month_strs = {
            1: "Января",
            2: "Февраля",
            3: "Марта",
            4: "Апреля",
            5: "Мая",
            6: "Июня",
            7: "Июля",
            8: "Августа",
            9: "Сентября",
            10: "Октября",
            11: "Ноября",
            12: "Декабря"
        }

        now_datetime = datetime.now(tz)
        format_string = "%d %s %d %d:%d"
        month_str = month_strs[now_datetime.month]
        
        _hms = now_datetime.hour, now_datetime.minute
        
        _h = _hms[0] if _hms[0] >= 10 else int('0' + str(_hms[0]))
        _m = _hms[1] if _hms[1] >= 10 else int('0' + str(_hms[1]))
        hms = _h, _m
        
        now_str = format_string % (now_datetime.day,
                            month_str,
                            now_datetime.year,
                            hms[0],
                            hms[1])
        
        embed = discord.Embed(color=discord.Color.purple(), title=now_str)
        embed.add_field(name='Доступные часовые пояса:', value=tzs[:-2])
        embed.set_footer(text=f"Часовой пояс - {city}")
        
        await mes.reply(embed=embed)
    elif command.startswith('hex'):
        colour = command.replace('hex ', '')
        emb = Embed(colour=Colour.from_str(colour),
                    description='Посмотри, нравится тебе этот цвет или нет ;)',
                    title=colour)
        
        await mes.reply(embed=emb)
    else:
        try:
            r = searchh(s)
        except:
            await mes.reply('Ошибка! Наверное, вы ввели неверный запрос')
        
        if isinstance(r, tuple):
            mes2 = await mes.reply('Ждём ответ от гугла...')

            emb, view = r    
            v = view(message=mes)

            await mes2.edit(embed=emb, view=v, content='Нашёл в интернете:')
        elif isinstance(r, Embed):
            await mes.reply(embed=r, content='Нашёл в интернете:')
        elif isinstance(r, str):
            await mes.reply(r)
        else:
            await mes.reply('DEV: No answer!')


def glue(tup) -> str:
    r = ''
    for i in tup:
        r += i
    return r

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


@bot.event
async def on_ready():
    guilds = bot.guilds

    for guild in guilds:
        member: discord.Member = guild.get_member(bot.user.id)
        await member.edit(nick="Sanyya | [A]")

    print("Hi?")

@bot.tree.command(description="Информация про бота")
async def инфо(interaction: discord.Interaction):
    text = (
        "Разработчики: `pixeldeee#3565`\n",
        "Оффициальный дискорд сервер: https://discord.gg/QsE5DSQrsx"
    )
    await interaction.response.send_message(glue(text), ephemeral=True)


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
            channel = bot.get_channel(1045560038149853235)
            
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
        description = ui.TextInput(label="Описание идеи",
                               style=discord.TextStyle.paragraph,
                               custom_id="des",
                               placeholder="Добавить команду /идея. С её помощью можно предложить идею.",
                               min_length=1,
                               max_length=2000)

        profile_for_connection = ui.TextInput(label="Профиль для связи",
                                              style=discord.TextStyle.short,
                                              custom_id="profile_for_connection",
                                              placeholder="name#1234",
                                              required=False,
                                              min_length=5,
                                              max_length=100)
        
        async def on_submit(self, interaction: discord.Interaction):
            channel = bot.get_channel(1045560087063830558)
            
            mes = str(self.description)

            if self.profile_for_connection.value:
                mes += (endl * 2) + "Профиль для связи: " + str(self.profile_for_connection)
            
            await channel.send(mes)
            
            await interaction.response.send_message('Спасибо!', ephemeral=True)
    
    await interaction.response.send_modal(IdeaModal())

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return

    if message.channel.id in channels or isinstance(message.channel, discord.DMChannel):
        message_types = (mt.reply, mt.default, mt.thread_starter_message)

        if not message.type in message_types: return
        if message.content.startswith('.'): return

        async with message.channel.typing():
            sleep(0.3)
        
        if message.content.startswith('!exs') and message.channel.id == 1046835447592136775: # Testing
            r = searchh(message.content.replace('!exs ', ''))
            
            if isinstance(r, tuple):
                mes = await message.reply('Awaiting answer of google...')
                
                emb = r[0]
                view = r[1]
                
                v = view(message=mes)
                
                await mes.edit(embed=emb, view=v, content='')
            elif isinstance(r, Embed):
                await message.reply(embed=r)
            else:
                await message.reply(r)
            return
        
        chatmode = channels_json[message.channel.id]
        go_to_chat = ["давай поболтаем", "давай поговорим", "го поболтаем", "го поговорим"]
        end_chat = ["хватит", "хватит болтать"]
        
        if chatmode is False:
            if message.content.lower() in go_to_chat:
                channels_json[message.channel.id] = True
                await message.reply('Отлично! Если вам надоест, напишите слово "Хватит"')
                member = message.guild.get_member(bot.user.id)
                await member.edit(nick="Sanya | [C]")
            else:
                await AssistentMessage(message)
        elif chatmode is True:
            if message.content.lower() in end_chat:
                channels_json[message.channel.id] = False
                await message.reply('Надоело? Если ещё захотите пообщаться, напишите "Давай поболтаем"')
                member = message.guild.get_member(bot.user.id)
                await member.edit(nick="Sanya | [A]")
            else:
                await message.reply(textMessage(message.content))

bot.run(os.environ['TOKEN'])
