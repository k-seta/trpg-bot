#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random

class DiceLogic:

    def __init__(self):
        pass

    @staticmethod
    def roll(amount, size):
        return [random.randint(1, size) for i in range(amount)]

    @staticmethod
    def roll_d66():
        return random.choice([11, 12, 13, 14, 15, 16, 12, 22, 23, 24, 25, 26, 13, 23, 33, 34, 35, 36, 14, 24, 34, 44, 45, 46, 15, 25, 35, 45, 55, 56, 16, 26, 36, 46, 56, 66])
