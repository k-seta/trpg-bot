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

    def dice(self, session, user, command):
        result, sum_dices = super().dice(session, author, command)
        if '<' in command:
            url = self.redis.hget(session, user)
            player = CthulhuPlayer(user, url)

            param_key = command.split('<')[1].strip()
            param_value = player.get(param_key)
            result += f" < {param_key}({param_value})"
        return result, sum_dices