#!/usr/bin/env python
#-*- coding:utf-8 -*-

import itertools
class DiceArgs:
    def __init__(self, value, items):
        if type(value) == int:
            self.value = value
        else:
            raise Exception('Type error: value')
        
        if type(items) == list:
            self.items = [items]
        elif type(items) == int:
            self.items = [[items]]
        else:
            raise Exception('Type error: items')

    def __add__(self, other):
        if type(other) == DiceArgs:
            self.value += other.value
            self.items += other.items
        elif type(other) == int:
            self.value += other
            self.items += [[other]]
        else:
            raise Exception('Type error: + operator')
        return self

    def __sub__(self, other):
        if type(other) == DiceArgs:
            self.value -= other.value
            self.items += other.items
        elif type(other) == int:
            self.value -= other
            self.items += [[other]]
        else:
            raise Exception('Type error: + operator')
        return self

    def __str__(self):
        if len(list(itertools.chain.from_iterable(self.items))) == 1:
            return f"{self.items[0][0]}"
        details = []
        for d in self.items:
            details.append(f"[{','.join([str(x) for x in d])}]")
        return f"{self.value}  {', '.join(details)}"
