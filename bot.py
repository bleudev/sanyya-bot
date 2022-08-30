"""
General file of bot
"""

import os
from random import choice
import discord
from api import main
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import re

TOKEN = os.environ["TOKEN"]

bot = discord.Client(intents=discord.Intents.all())
channels = [1008038030042484918, 1008080816166948865]


def clean_str(r):
    r = r.lower()
    r = [c for c in r if c in alphabet]
    return ''.join(r)

alphabet = ' 1234567890-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm?%.,()!:;'

def update():
    with open('dialogues.txt', encoding='utf-8') as f:
        content = f.read()
	
    blocks = content.split('\n')
    dataset = []
	
    for block in blocks:
        replicas = block.split('\\')[:2]
        if len(replicas) == 2:
            pair = [clean_str(replicas[0]), clean_str(replicas[1])]
            if pair[0] and pair[1]:
                dataset.append(pair)
	
    X_text = []
    y = []
	
    for question, answer in dataset[:10000]:
        X_text.append(question)
        y += [answer]
	
    global vectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_text)
	
    global clf
    clf = LogisticRegression()
    clf.fit(X, y)

update()

def get_generative_replica(text):
	text_vector = vectorizer.transform([text]).toarray()[0]
	question = clf.predict([text_vector])[0]
	return question


@bot.event
async def on_ready():
    print("Hi")


async def wrong(message):
    a = f"{question}\{message.text.lower()} \n"
    with open('dialogues.txt', "a", encoding='utf-8') as f:
        f.write(a)
    await message.channel.send("Готово!")
    update()


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel) or message.channel.id in channels:
        async with message.channel.typing():
            text: str = str(message.content).lower()
            
            if text =="не так":
                await message.reply("а как?")
                await wrong(message)
            else:
                global question
                question = text
                
                reply = get_generative_replica(text)
                
                await message.reply(reply)

bot.run(TOKEN)
