#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

from mode.DefaultMode import DefaultMode
from logic.DiceListLogic import DiceListLogic
from logic.DiceLogic import DiceLogic
from logic.CommandInterpreterLogic import CommandInterpreter
from player.MayokinPlayer import MayokinPlayer

class MayokinMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)

    def status(self, message):
        session = message.channel.name
        user = message.author.name
        url = self.redis.hget(session, user)
        player = MayokinPlayer(user, url)
        return player.print()

    def dice(self, message):
        match_d66, name = CommandInterpreter.match_d66(message.content)
        if match_d66:
            path = f"./trpg_bot/resources/mayokin/{name.strip()}.txt"
            value = DiceLogic.roll_d66()
            res_str = DiceListLogic.disp(path, value) if len(name) != 0 else value
            return res_str, value

        res_default, sum_dices = super().dice(message)
        match_ndn_txt, name = CommandInterpreter.match_ndn_txt(message.content)
        if match_ndn_txt:
            path = f"./trpg_bot/resources/mayokin/{name.strip()}.txt"
            list_item = DiceListLogic.disp(path, sum_dices)
            res_str = f"{res_default}\n{list_item}"
            return res_str, sum_dices
        return res_default, sum_dices