#!/usr/bin/env python
#-*- coding:utf-8 -*-

class DiceListLogic:

    def __init__(self):
        pass

    @staticmethod
    def disp(path_of_dice_list, value):
        list_as_str = ''
        with open(path_of_dice_list, 'r') as f:
            list_as_str = f.read()
        list_as_lst = list_as_str.splitlines()
        list_as_dict = {}
        for line in list_as_lst:
            splitted = line.split(': ')
            list_as_dict[splitted[0]] = line
        return list_as_dict[str(value)]
