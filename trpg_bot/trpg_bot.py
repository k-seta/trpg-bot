#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import random
import discord

def dice_ndn(message_ndn):
    pattern = '(\d+)d(\d+)'
    match_obj = re.search(pattern, message_ndn)
    if not match_obj:
        return []
    quantity = int(match_obj.group(1))
    size = int(match_obj.group(2))
    return [random.randint(1, size) for i in range(quantity)]

def validate_ndn(message):
    pattern = '^/.*?(\d+d\d+)'
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

        if validate_ndn(message.content):
            dice = dice_ndn(message.content)
            reply = f"{message.author.mention} がサイコロを降ったよ\n=> {sum(dice)} [{', '.join(map(str, dice))}]"
            await message.channel.send(reply)      

    client.run(TOKEN)
