#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import traceback
import discord
import redis

from logic import CommandInterpreterLogic, DropboxLogic, ModeSelectorLogic

if __name__ == '__main__':
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    REDIS = os.environ['REDIS_URL']
    DROPBOX_TOKEN = os.environ['DROPBOX_TOKEN']
    COMMIT_HASH = os.environ['HEROKU_SLUG_COMMIT'] if 'HEROKU_SLUG_COMMIT' in os.environ.keys() else 'None'

    client = discord.Client()
    r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

    mode_selector = ModeSelectorLogic(r)
    dbx = DropboxLogic(DROPBOX_TOKEN)

    @client.event
    async def on_ready():
        dbx.sync()
        print('activated trpg-bot client.')

    @client.event
    async def on_message(message):
        try:
            if message.author.bot:
                return

            guild = message.guild.name
            session = message.channel.name
            user  = message.author.name
            command, params = CommandInterpreterLogic().interp_command(message.content)
            
            if command == 'ping':
                await message.channel.send('pong')

            if command == 'debug':
                ls_dropbox = os.listdir('./trpg_bot/resources/mayokin')
                await message.channel.send(f"```\nrevision: {COMMIT_HASH}\nresources_dropbox: {ls_dropbox}```")

            if command == 'redis':
                reply = '\n'.join([key for key in r.scan_iter()])
                await message.channel.send(f"```\n{reply}```")

            if command == 'sync':
                await message.channel.send('Start syncing...')
                dbx.sync()
                await message.channel.send('Dice lists were synced with Dropbox.')

            if command == 'mode':
                mode_name = params[0]
                mode = mode_selector.select(guild, session, mode_name)
                await message.channel.send(f"{mode} モードになったよ")

            if command == 'help':
                help = mode_selector.get(guild, session).help()
                await message.channel.send(help)

            if command == 'regist':
                url = params[0]
                mode_selector.get(guild, session).regist(guild, session, user, url)
                await message.channel.send(f"{message.author.mention} がキャラシートを登録したよ\n=> {url}")

            if command == 'players':
                table = mode_selector.get(guild, session).players(guild, session)
                await message.channel.send(f"{message.channel.mention} のキャラシート一覧だよ\n```{table}```")

            if command == 'dice':
                result = mode_selector.get(guild, session).dice(session, user, params)
                await message.channel.send(f"{message.author.mention} がサイコロを振ったよ\n=> {result}")

            if command == 'status':
                status = mode_selector.get(guild, session).status(session, user)
                await message.channel.send(f"{message.author.mention} のキャラシートだよ\n```{status}```")

            if command == 'extra':
                result = mode_selector.get(guild, session).extra(params)
                if result != None:
                    await message.channel.send(result)

        except Exception as e:
            await message.channel.send(f"何かエラーが起きたみたいだよ\n```{str(e)}```")
            traceback.print_exc()

    @client.event
    async def on_guild_channel_delete(channel):
        try:
            r.hdel('mode', channel.name)
            r.delete(channel.name)
        except Exception as e:
            traceback.print_exc()

    client.run(TOKEN)
