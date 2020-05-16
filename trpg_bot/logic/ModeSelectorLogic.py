#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode.DefaultMode import DefaultMode
from mode.CthulhuMode import CthulhuMode

class ModeSelectorLogic:

    def __init__(self, redis):
        self.redis = redis
        self.modes = { 
            'default': DefaultMode(self.redis, './trpg_bot/resources/usage_default.md'),
            'cthulhu': CthulhuMode(self.redis, './trpg_bot/resources/usage_cthulhu.md')
        }

    def get(self, message):
        session = message.channel.name
        key = self.redis.hget('mode', session)
        print(key)
        if key == None or not key in self.modes.keys():
            key = 'default'
        return self.modes[key]

    def select(self, message, key):
        session = message.channel.name
        mode = 'default'
        if key in ['cthulhu', 'クトゥルフ']:
            mode = 'cthulhu'
        print(mode)
        self.redis.hset('mode', session, mode)
