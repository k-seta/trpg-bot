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
from prettytable import PrettyTable

from player.CthulhuPlayer import CthulhuPlayer

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

def validate_regist(message):
    pattern = '^/regist (http.*)'
    return re.match(pattern, message)

def validate_ndn(message):
    pattern = '^/.*?(\d+d\d+)'
    return re.match(pattern, message)

if __name__ == '__main__':
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    REDIS = os.environ['REDIS_URL']

    GLOBAL_CHANNEL_ID = int(os.environ['GLOBAL_CHANNEL_ID'])

    client = discord.Client()
    r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

    reply_help = ''
    with open('./trpg_bot/usage.md', 'r') as f:
        reply_help = f.read()

    @client.event
    async def on_ready():
        print('activated trpg-bot client.')

    @client.event
    async def on_message(message):
        try:
            if message.author.bot:
                return

            if message.content == '/ping':
                await message.channel.send('pong')

            if message.content == '/redis':
                reply='\n'
                for key in r.scan_iter():
                   reply += f"{key}\n"
                print(reply)
                await message.channel.send(f"```{reply}```")

            if message.content == '/help':
                await message.channel.send(reply_help)

            match_regist = validate_regist(message.content)
            if match_regist:
                session = message.channel.name
                user = message.author.name
                url = match_regist.group(1)
                r.hset(session, user, url)
                reply = f"{message.author.mention} がキャラシートを登録したよ\n=> {url}"
                await message.channel.send(reply)

            if message.content == '/players':
                session = message.channel.name
                data = r.hgetall(session)
                table = PrettyTable()
                table.field_names = ['user', 'url']
                for user, url in data.items():
                    table.add_row([user, url])
                await message.channel.send(f"{message.channel.mention} のキャラシート一覧だよ\n```{table.get_string()}```")

            if validate_ndn(message.content):
                elements = message.content.split('+')
                dices = [dice_ndn(e) for e in elements]
                sum_dices = sum(list(itertools.chain.from_iterable(dices)))
                reply = f"{message.author.mention} がサイコロを振ったよ\n=> {sum_dices}    {str(dices)[1:-1]}"
                
                if '<' in message.content:
                    session = message.channel.name
                    user = message.author.name
                    url = r.hget(session, user)
                    player = CthulhuPlayer(user, url)

                    param_key = message.content.split('<')[1].strip()
                    param_value = player.get(param_key)
                    reply += f" < {param_key}({param_value})"
                await message.channel.send(reply)

            if message.content == '/status':
                session = message.channel.name
                user = message.author.name
                url = r.hget(session, user)
                player = CthulhuPlayer(user, url)
                status = player.print()
                await message.channel.send(f"{message.author.mention} のキャラシートだよ\n```{status}```")

        except Exception as e:
            await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
            traceback.print_exc()

    @client.event
    async def on_guild_channel_delete(channel):
        try:
            r.delete(channel.name)
            global_channel = client.get_channel(GLOBAL_CHANNEL_ID)
            await global_channel.send(f"{message.channel.mention}のプレイヤーデータを削除したよ")

        except Exception as e:
            await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
            traceback.print_exc()

    client.run(TOKEN)
