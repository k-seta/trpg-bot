#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import discord

TOKEN = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print('activated lavoce-trpg-bot client.')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/ping':
        await message.channel.send('pong')

client.run(TOKEN)
