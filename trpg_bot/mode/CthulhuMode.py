#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode import DefaultMode
from player import CthulhuPlayer
from logic import DiceLogic, CommandInterpreterLogic

class CthulhuMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)

    def status(self, message):
        session = message.channel.name
        user = message.author.name
        url = self.redis.hget(session, user)
        player = CthulhuPlayer(user, url)
        return player.print()

    def dice(self, session, user, tokens):

        url = self.redis.hget(session, user)
        player = CthulhuPlayer(user, url)

        prop_names = []

        def proc(token):

            is_ndn, (amount, size) = CommandInterpreterLogic.match_ndn(token)
            if is_ndn:
                prop_names.append('')
                return DiceLogic.roll(amount, size)
            
            is_d66, _ = CommandInterpreterLogic.match_d66(token)
            if is_d66:
                prop_names.append('')
                return [DiceLogic.roll_d66()]
            
            is_const, (const,) = CommandInterpreterLogic.match_const(token)
            if is_const:
                prop_names.append('')
                return [const]
            
            prop_val = player.get(token)
            if prop_val:
                prop_names.append(token)
                return [int(prop_val)]

            # 存在しない技能値/演算子
            prop_names.append(token)
            return [0]
        
        result_values = [proc(token) for token in tokens]

        left_vals, left_sum = '', 0
        op = ''
        right_vals, right_sum = '', 0

        for key, val in zip(prop_names, result_values):
            if key == '+':
                continue
            if key in ['<', '>']:
                op = key
                continue

            if op == '':
                if key == '':
                    left_vals += f"{str(val)}"
                else:
                    left_vals += f"[{key} {str(val[0])}]"
                left_sum  += sum(val)
            else:
                if key == '':
                    right_vals += f"{str(val)}"
                else:
                    right_vals += f"[{key} {str(val[0])}]"
                right_sum  += sum(val)

        if op:
            return f"{left_sum}  {left_vals} {op} {right_sum}  {right_vals}"
        else:
            return f"{left_sum}  {left_vals}"