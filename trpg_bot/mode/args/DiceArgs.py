#!/usr/bin/env python
#-*- coding:utf-8 -*-

class DiceArgs:
    def __init__(self, value, items):
        if type(value) == int:
            self.value = value
        else:
            raise Exception('Type error: value')
        
        if type(items) == list:
            self.items = items
        elif type(items) == int:
            self.items = [items]
        else:
            raise Exception('Type error: items')

    def __add__(self, other):
        if type(other) == DiceArgs:
            self.value += other.value
            self.items.append(other.items)
        elif type(other) == int:
            self.value += other
            self.items.append([other])
        else:
            raise Exception('Type error: + operator')

    def __str__(self):
        return f"{self.value}  {str(self.items)[1:-1]}"
