#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import itertools

import redis
from prettytable import PrettyTable

from logic import DiceLogic, CommandInterpreterLogic
from .args import DiceArgs, FunctionalDiceArgs

class DefaultMode:

    def __init__(self, redis, path_of_help_md):
        self.redis = redis
        with open(path_of_help_md, 'r') as f:
            self.message_help = f.read()

    def help(self):
        return self.message_help

    def regist(self, guild, session, user, url):
        self.redis.hset(f"{guild}.{session}", user, url)

    def players(self, guild, session):
        data = self.redis.hgetall(f"{guild}.{session}")
        table = PrettyTable()
        table.field_names = ['user', 'url']
        for user, url in data.items():
            table.add_row([user, url])
        return table.get_string()

    def status(self, guild, session, user):
        return 'モード未指定のためこの機能は使用できません'

    def dice(self, session, user, tokens):

        def proc(token):
            if type(token) == DiceArgs or type(token) == FunctionalDiceArgs:
                return token
            is_ndn, (amount, size) = CommandInterpreterLogic.match_ndn(token)
            if is_ndn:
                res = DiceLogic.roll(amount, size)
                return DiceArgs(sum(res), res)
            is_d66, _ = CommandInterpreterLogic.match_d66(token)
            if is_d66:
                res = DiceLogic.roll_d66()
                return DiceArgs(res, res)
            is_const, (const,) = CommandInterpreterLogic.match_const(token)
            if is_const:
                return DiceArgs(const, const)
            return token

        result_dices = [proc(token) for token in tokens]
        result_values = []
        while len(result_dices) > 0:
            head = result_dices.pop(0)
            if type(head) == FunctionalDiceArgs:
                value = result_values[-1]
                result_values.append(head.to_dice_args(value))
            elif head == '+':
                left = result_values.pop(-1)
                right = result_dices.pop(0)
                result_values.append(left + right)
            elif head == '-':
                left = result_values.pop(-1)
                right = result_dices.pop(0)
                result_values.append(left - right)
            else:
                result_values.append(head)
        return ' '.join([str(value) for value in result_values])

    def extra(self, params):
        return None
