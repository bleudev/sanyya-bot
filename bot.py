"""
General file of bot
"""

import os
import disspy

TOKEN = os.environ["TOKEN"]

bot = disspy.DisBot(token=TOKEN, status="dnd", flags=disspy.DisFlags.messages(), debug=True)


@bot.on_ready()
async def on_ready():
    print("Hi")


@bot.on_channel(1008038030042484918)
async def chat(message: disspy.DisMessage):
    await message.channel.typing()

    await message.reply("Приветик!")


bot.run()
