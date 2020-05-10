#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode.DefaultMode import DefaultMode
from mode.CthulhuMode import CthulhuMode

class ModeSelectorLogic:

    def __init__(self, redis):
        self.redis = redis
        self.mode = DefaultMode(redis, './trpg_bot/resources/usage_default.md')

    def get(self):
        return self.mode

    def select(self, key):
        if key in ['default', 'デフォルト']:
            self.mode = DefaultMode(self.redis, './trpg_bot/resources/usage_default.md')
        if key in ['cthulhu', 'クトゥルフ']:
            self.mode = CthulhuMode(self.redis, './trpg_bot/resources/usage_cthulhu.md')
