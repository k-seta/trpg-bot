#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random

class DiceLogic:

    def __init__(self):
        pass

    @staticmethod
    def roll(amount, size):
        return [random.randint(1, size) for i in range(amount)]
