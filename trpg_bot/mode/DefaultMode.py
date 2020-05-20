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

    def calc(self, message):
        raise Exception('Invalid mode')

    def choice(self, message):
        raise Exception('Invalid mode')

    # Internal processes

    def _calc_internal(self, message, player):
        """
        ['/', [23], '+', [10], '+', 'SAN', '<', [100]]
          => ['/', [23], '+', [10], '+', [64], '<', [100]]
          => '97 [23][10][SAN 64] < 100 [100]'
        """
        session = message.channel.name
        user = message.author.name
        url = self.redis.hget(session, user)

        intermediate_tokens = self._dice_internal(message)
        calced_tokens = [[int(player.get(str(c)))] if player.get(str(c)) else c for c in calc_results]

        left_res, left_sum = '', 0
        op = ''
        right_res, right_sum = '', 0

        for prev, res in zip(intermediate_tokens, calced_tokens):

            if res in ['+', '/']:
                continue

            if res in ['=', '<', '>']:
                op = res
                continue

            if op == '':
                if type(prev) is str:
                    left_res += f"{prev} {res[0]}"
                else:
                    left_res += f"{str(res)}"
                left_sum += sum(res)
            else:
                if type(prev) is str:
                    right_res += f"{prev} {res[0]}"
                else:
                    right_res += f"{str(res)}"
                right_sum += sum(res)
            
        if op:
            return f"{left_sum}   {left_res} {op} {right_sum}    {right_res}"
        else:
            return f"{left_sum}   {left_res}"

    def _dice_internal(self, message):
        """
        '/1d50+10+SAN<100'
          => ['/', '1d50', '+', '10', '+', 'SAN', '<', '100']
          => ['/', [23], '+', [10], '+', 'SAN', '<', [100]]
        """
        terms = CommandInterpreterLogic.parse_dices(message.content)

        def calc_term(term):

            is_ndn, (amount, size) = CommandInterpreterLogic.match_ndn(term)
            if is_ndn:
                return DiceLogic.roll(amount, size)

            is_d66, _ = CommandInterpreterLogic.match_d66(term)
            if is_d66:
                return [DiceLogic.roll_d66()]

            is_const, (const,) = CommandInterpreterLogic.match_const(term)
            if const:
                return [const]

            return term
            
        res = [calc_term(term) for term in terms]
        return res