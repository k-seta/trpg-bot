#!/usr/bin/env python
#-*- coding:utf-8 -*-

from . import DiceArgs

class FunctionalDiceArgs:
    def __init__(self, func):
        if type(func).__name__ == 'function':
            self.func = func
        else:
            raise Exception('Type error: func')

    def to_dice_args(self, var):
        if type(var) == int:
            return DiceArgs(var, [self.func(var)])
        elif type(var) == DiceArgs:
            return DiceArgs(var.value, [self.func(var.value)])
        else:
            raise Exception('Type error: var')
