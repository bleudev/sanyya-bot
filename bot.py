"""
General file of bot
"""

import os
import disspy
from api import main
from random import choice

TOKEN = os.environ["TOKEN"]

bot = disspy.DisBot(token=TOKEN, status="dnd", flags=disspy.DisFlags.messages())


@bot.on_ready()
async def on_ready():
    print("Hi")


@bot.on_channel(1008038030042484918)  # Official discord server chatting channel
async def chat(message: disspy.DisMessage):
    await message.channel.typing()

    text: str = str(main(message.content))

    if text == "None":
        text = choice(["О чём ты?", "Я не понимаю вас", "Что?"])

    await message.reply(text)


@bot.on_dm_message("create")
async def dm_chat(message: disspy.DmMessage):
    # await message.channel.typing() # Typing is not supported in Dm channels

    text: str = str(main(message.content))

    if text == "None":
        text = choice(["О чём ты?", "Я не понимаю вас", "Что?"])

    await message.reply(text)


bot.run()
