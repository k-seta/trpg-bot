#!/usr/bin/env python
#-*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod

class AbstractPlayer(metaclass=ABCMeta):

    @abstractmethod
    def get(self, param):
        pass

    @abstractmethod
    def print(self):
        pass
