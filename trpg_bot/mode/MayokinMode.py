#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

from mode.DefaultMode import DefaultMode
from logic.DiceListLogic import DiceListLogic
from logic.DiceLogic import DiceLogic
from logic.CommandInterpreterLogic import CommandInterpreterLogic
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

    def calc(self, message):
        session = message.channel.name
        user = message.author.name
        url = self.redis.hget(session, user)
        player = MayokinPlayer(user, url)
        return self._calc_internal(message, player)

    def choice(self, message):
        calced_tokens = self._dice_internal(message)

        left_sum = 0
        op = ''
        right_list_name = ''

        for token in calced_tokens:

            if token in ['/', '+']:
                continue

            if token == '=':
                op = token
                continue

            if op == '':
                left_sum += sum(token)
            else:
                right_list_name = token
        
        path = f"./trpg_bot/resources/mayokin/{right_list_name}.txt"
        return DiceListLogic.disp(path, left_sum)
