#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import random
import itertools
import traceback
import discord
import json
import redis

def dice_ndn(message_ndn):
    pattern_dice = '(\d+)d(\d+)'
    match_dice = re.search(pattern_dice, message_ndn)
    if not match_dice:
        pattern_const = '(\d+)'
        match_const = re.search(pattern_const, message_ndn)
        return [int(match_const.group(1))] if match_const else []
    quantity = int(match_dice.group(1))
    size = int(match_dice.group(2))
    return [random.randint(1, size) for i in range(quantity)]

def validate_ndn(message):
    pattern = '^/.*?(\d+d\d+)'
    return re.match(pattern, message)

if __name__ == '__main__':
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    REDIS = os.environ['REDIS_URL']

    client = discord.Client()
    r = redis.from_url(os.environ.get("REDIS_URL"))

    @client.event
    async def on_ready():
        print('activated trpg-bot client.')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        if message.content == '/ping':
            await message.channel.send('pong')

        if message.content == '/regist':
            r.hmset('test', {'name': 'Taro'})
            await message.channel.send('registered.')

        if message.content == '/players':
            reply = r.hgetall('test')
            r.delete('test')
            await message.channel.send(json.dumps(reply))

        if validate_ndn(message.content):
            elements = message.content.split('+')
            dices = [dice_ndn(e) for e in elements]
            sum_dices = sum(list(itertools.chain.from_iterable(dices)))
            reply = f"{message.author.mention} がサイコロを振ったよ\n=> {sum_dices}    {str(dices)[1:-1]}"
            try:
                await message.channel.send(reply)      
            except Exception as e:
                await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
                traceback.print_exc()

    client.run(TOKEN)
