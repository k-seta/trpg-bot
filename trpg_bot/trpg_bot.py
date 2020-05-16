#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import traceback
import discord
import redis
import dropbox

from logic.ModeSelectorLogic import ModeSelectorLogic

def validate_mode(message):
    pattern = '^/mode (.*)'
    return re.match(pattern, message)

def validate_regist(message):
    pattern = '^/regist (http.*)'
    return re.match(pattern, message)

def validate_ndn(message):
    pattern = '^/.*?(\d*d\d+)'
    return re.match(pattern, message)

if __name__ == '__main__':
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    REDIS = os.environ['REDIS_URL']
    GLOBAL_CHANNEL_ID = int(os.environ['GLOBAL_CHANNEL_ID'])
    DROPBOX_TOKEN = os.environ['DROPBOX_TOKEN']

    client = discord.Client()
    r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    entries = dbx.files_list_folder('/mayokin').entries
    for entry in entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            dbx.files_download_to_file(f"./trpg_bot/resources/mayokin/{entries[0].name}", entries[0].path_lower)
            print(f"downloaded {entries[0].path_lower}")

    mode_selector = ModeSelectorLogic(r)

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
                await message.channel.send(f"```{reply}```")

            match_mode = validate_mode(message.content)
            if match_mode:
                key = match_mode.group(1)
                mode = mode_selector.select(message, key)
                await message.channel.send(f"{mode} モードになったよ")

            if message.content == '/help':
                reply = mode_selector.get(message).help()
                await message.channel.send(reply)

            match_regist = validate_regist(message.content)
            if match_regist:
                url = match_regist.group(1)
                mode_selector.get(message).regist(message, url)
                await message.channel.send(f"{message.author.mention} がキャラシートを登録したよ\n=> {url}")

            if message.content == '/players':
                table = mode_selector.get(message).players(message)
                await message.channel.send(f"{message.channel.mention} のキャラシート一覧だよ\n```{table}```")

            if validate_ndn(message.content):
                result = mode_selector.get(message).dice(message)
                reply = f"{message.author.mention} がサイコロを振ったよ\n=> {result}"
                await message.channel.send(reply)

            if message.content == '/status':
                status = mode_selector.get(message).status(message)
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
