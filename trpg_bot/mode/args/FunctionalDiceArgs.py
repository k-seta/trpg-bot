#!/usr/bin/env python
#-*- coding:utf-8 -*-

from . import DiceArgs

class FunctionalDiceArgs:
    def __init__(self, func, var_relative_index):
        if type(func).__name__ == 'function':
            self.func = func
        else:
            raise Exception('Type error: func')
        
        # self.func の引数となる値の相対index
        if type(var_relative_index) == int:
            self.var_relative_index = (var_relative_index)
        elif type(var_relative_index) == tuple or type(var_relative_index) == list:
            self.var_relative_index = var_relative_index
        else:
            raise Exception('Type error: var_relative_index')

    def to_dice_args(self, var):
        if type(var) == int:
            return DiceArgs(var, [self.func(var)])
        elif type(var) == DiceArgs:
            return DiceArgs(var.value, [self.func(var.value)])
        else:
            raise Exception('Type error: var')
