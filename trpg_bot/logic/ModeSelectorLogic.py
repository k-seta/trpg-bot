#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode import DefaultMode, CthulhuMode, MayokinMode

class ModeSelectorLogic:

    def __init__(self, redis):
        self.redis = redis
        self.modes = { 
            'default': DefaultMode(self.redis, './trpg_bot/resources/usage_default.md'),
            'cthulhu': CthulhuMode(self.redis, './trpg_bot/resources/usage_cthulhu.md'),
            'mayokin': MayokinMode(self.redis, './trpg_bot/resources/usage_mayokin.md')
        }

    def get(self, message):
        session = message.channel.name
        key = self.redis.hget('mode', session)
        if key == None or not key in self.modes.keys():
            key = 'default'
        return self.modes[key]

    def select(self, message, key):
        session = message.channel.name
        mode = 'default'
        if key in ['cthulhu', 'クトゥルフ']:
            mode = 'cthulhu'
        if key in ['mayokin', 'マヨキン']:
            mode = 'mayokin'
        self.redis.hset('mode', session, mode)
        return mode
