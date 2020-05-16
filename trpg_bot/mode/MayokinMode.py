#!/usr/bin/env python
#-*- coding:utf-8 -*-

from mode.DefaultMode import DefaultMode

class MayokinMode(DefaultMode):

    def __init__(self, redis, path_of_help_md):
        super().__init__(redis, path_of_help_md)
