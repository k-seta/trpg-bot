#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

from mode.DefaultMode import DefaultMode
from logic.DiceListLogic import DiceListLogic
from logic.DiceLogic import DiceLogic

class MayokinMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)

    def dice(self, message):
        match_d66 = re.search('/d66(.*)', message.content)
        if match_d66:
            name = match_d66.group(1).strip()
            path = f"./trpg_bot/resources/mayokin/{name}.txt"
            value = DiceLogic.roll_d66()
            return DiceListLogic.disp(path, value) if len(name) != 0 else value

        result, sum_dices = super().dice(message)
        match_ndn = re.search('\d+d\d+ (.+)', message.content)
        if match_ndn:
            name = match_ndn.group(1).strip()
            path = f"./trpg_bot/resources/mayokin/{name}.txt"
            list_item = DiceListLogic.disp(path, sum_dices)
            return f"{result}\n{list_item}"
        return result