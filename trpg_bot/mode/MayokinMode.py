#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

from mode import DefaultMode
from logic import DiceLogic, DiceListLogic, CommandInterpreterLogic
from player import MayokinPlayer
from .args import DiceArgs, FunctionalDiceArgs

class MayokinMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)

    def status(self, guild, session, user):
        url = self.redis.hget(f"{guild}.{session}", user)
        player = MayokinPlayer(user, url)
        return player.print()

    def dice(self, guild, session, user, tokens):

        url = self.redis.hget(f"{guild}.{session}", user)
        player = MayokinPlayer(user, url)

        def proc(token):
            val = player.get(token)
            if val != '':
                return DiceArgs(int(val), [f"{token}({val})"])            
            if '表' in token:
                dice_dict = DiceListLogic.get_dict(f"./trpg_bot/resources/mayokin/{token.strip()}.txt")
                return FunctionalDiceArgs(lambda var: f"\n{dice_dict[str(var)]}")
            return token
        
        result_props = [proc(token) for token in tokens]
        return super().dice(guild, session, user, result_props)
