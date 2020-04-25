#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import discord

def validate_ndn(message):
    pattern = '/(\d+?)d(\d+?)'
    return re.match(pattern, message)

if __name__ == '__main__':
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    client = discord.Client()

    @client.event
    async def on_ready():
        print('activated trpg-bot client.')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.content == '/ping':
            await message.channel.send('pong')

        match_obj = validate_ndn(message.content)
        if match_obj:
            await message.channel.send('dice')      

    client.run(TOKEN)
