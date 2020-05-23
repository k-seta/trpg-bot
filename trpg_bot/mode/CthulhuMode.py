#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode import DefaultMode
from player import CthulhuPlayer
from logic import DiceLogic, CommandInterpreterLogic
from .args import DiceArgs

class CthulhuMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)

    def status(self, message):
        session = message.channel.name
        user = message.author.name
        url = self.redis.hget(session, user)
        player = CthulhuPlayer(user, url)
        return player.print()

    def dice(self, session, user, tokens):

        url = self.redis.hget(session, user)
        player = CthulhuPlayer(user, url)

        def proc(token):
            val = player.get(token)
            if val != '':
                return DiceArgs(int(val), [f"{token}({val})"])
            return token
        
        result_props = [proc(token) for token in tokens]
        return super().dice(session, user, result_props)
