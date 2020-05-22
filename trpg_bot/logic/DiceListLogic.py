#!/usr/bin/env python
#-*- coding:utf-8 -*-

class DiceListLogic:

    def __init__(self):
        pass

    @staticmethod
    def disp(path_of_dice_list, value):
        return self.get_dict(path_of_dice_list)[str(value)]

    @staticmethod
    def get_dict(path_of_dice_list):
        list_as_str = ''
        with open(path_of_dice_list, 'r') as f:
            list_as_str = f.read()
        list_as_lst = list_as_str.splitlines()
        list_as_dict = {}
        for line in list_as_lst:
            splitted = line.split(': ')
            list_as_dict[splitted[0]] = splitted[1]
        return list_as_dict
