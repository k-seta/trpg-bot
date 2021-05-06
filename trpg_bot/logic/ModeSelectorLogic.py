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

    def get(self, guild, session):
        key = self.redis.hget(f"{guild}.mode", session)
        if key == None or not key in self.modes.keys():
            key = 'default'
        return self.modes[key]

    def select(self, guild, session, key):
        mode = 'default'
        if key in ['cthulhu', 'クトゥルフ']:
            mode = 'cthulhu'
        if key in ['mayokin', 'マヨキン']:
            mode = 'mayokin'
        self.redis.hset(f"{guild}.mode", session, mode)
        return mode
