#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import itertools

import redis
from prettytable import PrettyTable

from logic.DiceLogic import DiceLogic
from logic.CommandInterpreterLogic import CommandInterpreterLogic

class DefaultMode:

    def __init__(self, redis, path_of_help_md):
        self.redis = redis
        with open(path_of_help_md, 'r') as f:
            self.message_help = f.read()

    def help(self):
        return self.message_help

    def regist(self, message, url):
        session = message.channel.name
        user = message.author.name
        self.redis.hset(session, user, url)

    def players(self, message):
        session = message.channel.name
        data = self.redis.hgetall(session)
        table = PrettyTable()
        table.field_names = ['user', 'url']
        for user, url in data.items():
            table.add_row([user, url])
        return table.get_string()

    def status(self, message):
        return 'モード未指定のためこの機能は使用できません'

    def dice(self, session, user, command):
        dices = []
        terms = command.split('+')
        for e in terms:
            is_ndn, (amount, size) = CommandInterpreterLogic.match_ndn(e)
            if is_ndn:
                dices.append(DiceLogic.roll(amount, size))
                continue
            is_const, (const,) = CommandInterpreterLogic.match_const(e)
            if const:
                dices.append([const])

        sum_dices = sum(list(itertools.chain.from_iterable(dices)))
        return f"{sum_dices}    {str(dices)[1:-1]}", sum_dices
