#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

from mode.DefaultMode import DefaultMode
from logic.DiceListLogic import DiceListLogic
from logic.DiceLogic import DiceLogic
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
        match_d66 = re.search('/d66(.*)', message.content)
        if match_d66:
            name = match_d66.group(1).strip()
            path = f"./trpg_bot/resources/mayokin/{name}.txt"
            value = DiceLogic.roll_d66()
            res_str = DiceListLogic.disp(path, value) if len(name) != 0 else value
            return res_str, value

        res_default, sum_dices = super().dice(message)
        match_ndn = re.search('\d+d\d+ (.+)', message.content)
        if match_ndn:
            name = match_ndn.group(1).strip()
            path = f"./trpg_bot/resources/mayokin/{name}.txt"
            list_item = DiceListLogic.disp(path, sum_dices)
            res_str = f"{res_default}\n{list_item}"
            return res_str, sum_dices
        return res_default, sum_dices