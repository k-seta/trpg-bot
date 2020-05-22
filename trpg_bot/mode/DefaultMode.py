#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import itertools

import redis
from prettytable import PrettyTable

from logic import DiceLogic, CommandInterpreterLogic
from .args import DiceArgs

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

    def dice(self, session, user, tokens):

        def proc(token):
            if type(token) == DiceArgs:
                return token
            is_ndn, (amount, size) = CommandInterpreterLogic.match_ndn(token)
            if is_ndn:
                res = DiceLogic.roll(amount, size)
                return DiceArgs(sum(res), res)
            is_d66, _ = CommandInterpreterLogic.match_d66(token)
            if is_d66:
                res = DiceLogic.roll_d66()
                return DiceArgs(sum(res), res)
            is_const, (const,) = CommandInterpreterLogic.match_const(token)
            if is_const:
                return DiceArgs(const, const)
            return token

        result_dices = [proc(token) for token in tokens]
        result_values = []
        for i, x in enumerate(result_dices):
            if x == '+' and i > 0:
                result_values.append(result_values.pop(-1) + result_dices[i+1])
                continue
            elif result_dices[i-1] == '+' and i > 0:
                continue
            result_values.append(x)
        return ' '.join([str(value) for value in result_values])
