#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import itertools

import redis
from prettytable import PrettyTable

from logic.DiceLogic import DiceLogic

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

    def dice(self, message):
        dices = []
        terms = message.content.split('+')
        for e in terms:
            match_ndn = re.search('(\d+)d(\d+)', e)
            if match_ndn:
                amount = int(match_ndn.group(1))
                size = int(match_ndn.group(2))
                dices.append(DiceLogic.roll(amount, size))
                continue
            match_const = re.search('(\d+)', e)
            if match_const:
                dices.append([int(match_const.group(1))] if match_const else [])

        sum_dices = sum(list(itertools.chain.from_iterable(dices)))
        return f"{sum_dices}    {str(dices)[1:-1]}"
