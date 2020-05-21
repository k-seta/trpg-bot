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

    def dice(self, session, author, tokens):

        def roll(token):
            is_ndn, (amount, size) = CommandInterpreterLogic.match_ndn(token)
            if is_ndn:
                return DiceLogic.roll(amount, size)
            
            is_d66, _ = CommandInterpreterLogic.match_d66(token)
            if is_d66:
                return [DiceLogic.roll_d66()]
            
            is_const, (const,) = CommandInterpreterLogic.match_const(token)
            if is_const:
                return [const]

            return token
        
        result_values = [roll(token) for token in tokens]

        left_vals, left_sum = '', 0
        op = ''
        right_vals, right_sum = '', 0

        for val in result_values:
            if val == '+':
                continue
            if val in ['<', '>']:
                op = val
                continue

            if type(val) is str:
                raise Exception(f"Defaultモードでは扱えないトークンです: {val}")

            if op == '':
                left_vals += f"{str(val)}"
                left_sum  += sum(val)
            else:
                right_vals += f"{str(val)}"
                right_sum  += sum(val)

        if op:
            return f"{left_sum}  {left_vals} {op} {right_sum}  {right_vals}"
        else:
            return f"{left_sum}  {left_vals}"
