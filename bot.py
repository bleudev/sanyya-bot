"""
General file of bot
"""

import os
from random import choice
import discord
from api import main

TOKEN = os.environ["TOKEN"]

bot = discord.Client()
channels = [1008038030042484918]


@bot.event
async def on_ready():
    print("Hi")


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.DMChannel) or message.channel.id in channels:
        await message.channel.typing()

        text: str = str(main(message.content))

        if text == "None":
            text = choice(["О чём ты?", "Я не понимаю вас", "Что?"])

        await message.reply(text)

bot.run(TOKEN)
