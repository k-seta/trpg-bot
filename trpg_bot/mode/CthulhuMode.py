#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode.DefaultMode import DefaultMode
from player.CthulhuPlayer import CthulhuPlayer

class CthulhuMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)

    def status(self, message):
        session = message.channel.name
        user = message.author.name
        url = self.redis.hget(session, user)
        player = CthulhuPlayer(user, url)
        return player.print()

    def dice(self, message):
        result, sum_dices = super().dice(message)
        if '<' in message.content:
            session = message.channel.name
            user = message.author.name
            url = self.redis.hget(session, user)
            player = CthulhuPlayer(user, url)

            param_key = player.convert_arts_name(message.content.split('<')[1].strip())
            param_value = player.get(param_key)
            result += f" < {param_key}({param_value})"
        return result, sum_dices