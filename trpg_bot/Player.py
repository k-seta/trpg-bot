#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import requests
from prettytable import PrettyTable

class Player:

    user = 'user'
    url = 'url'

    name = 'name'

    HP = 0
    MP = 0
    SAN_MAX = 0
    IDA = 0
    LUK = 0
    ACK = 0


    STR = 0
    CON = 0
    POW = 0
    DEX = 0
    APP = 0
    SIZ = 0
    INT = 0 
    EDU = 0

    pattern_map = {
        'name': '<input name="pc_name" class="str" id="pc_name" size="55" type="text" value="(.*)"></td>',
        'HP': '<input name="NP9" id="NP9" value="(\d+)" size="3" readonly="true" type="text">',
        'MP': '<input name="NP10" id="NP10" value="(\d+)" size="3" readonly="true" type="text">',
        'SAN_LEFT': '<input type="text" name="SAN_Left" value="(\d+)" size="3" .*?>',
        'SAN_MAX': '<input name="NP11" id="NP11" value="(\d+)" size="3" readonly="true" type="text">',
        'IDA': '<input name="NP12" id="NP12" value="(\d+)" size="3" readonly="true" type="text">',
        'LUK': '<input name="NP13" id="NP13" value="(\d+)" size="3" readonly="true" type="text">',
        'ACK': '<input name="NP14" id="NP14" value="(\d+)" size="3" readonly="true" type="text">',
        'STR': '<input name="NP1" id="NP1" value="(\d+)" size="3" readonly="true" type="text">',
        'CON': '<input name="NP2" id="NP2" value="(\d+)" size="3" readonly="true" type="text">',
        'POW': '<input name="NP3" id="NP3" value="(\d+)" size="3" readonly="true" type="text">',
        'DEX': '<input name="NP4" id="NP4" value="(\d+)" size="3" readonly="true" type="text">',
        'APP': '<input name="NP5" id="NP5" value="(\d+)" size="3" readonly="true" type="text">',
        'SIZ': '<input name="NP6" id="NP6" value="(\d+)" size="3" readonly="true" type="text">',
        'INT': '<input name="NP7" id="NP7" value="(\d+)" size="3" readonly="true" type="text">',
        'EDU': '<input name="NP8" id="NP8" value="(\d+)" size="3" readonly="true" type="text">'
    }

    def __init__(self, user, url):
        self.user = user
        self.url = url

        res = requests.get(self.url)
        self.name = self.extract_status(res.text, 'name')

        self.HP = self.extract_status(res.text, 'HP')
        self.MP = self.extract_status(res.text, 'MP')
        self.SAN_LEFT = self.extract_status(res.text, 'SAN_LEFT')
        self.SAN_MAX = self.extract_status(res.text, 'SAN_MAX')
        self.IDA = self.extract_status(res.text, 'IDA')
        self.LUK = self.extract_status(res.text, 'LUK')
        self.ACK = self.extract_status(res.text, 'ACK')

        self.STR = int(self.extract_status(res.text, 'STR'))
        self.CON = int(self.extract_status(res.text, 'CON'))
        self.POW = int(self.extract_status(res.text, 'POW'))
        self.DEX = int(self.extract_status(res.text, 'DEX'))
        self.APP = int(self.extract_status(res.text, 'APP'))
        self.SIZ = int(self.extract_status(res.text, 'SIZ'))
        self.INT = int(self.extract_status(res.text, 'INT'))
        self.EDU = int(self.extract_status(res.text, 'EDU'))

    def extract_status(self, text, status):
        match_obj = re.search(self.pattern_map[status], text)
        return match_obj.group(1)

    def print(self):
        table = PrettyTable()
        table.field_names = ['HP', 'MP', 'IDA', 'LUK', 'ACK']
        table.add_row([self.HP, self.MP, self.IDA, self.LUK, self.ACK])
        mutable_status = table.get_string()

        table = PrettyTable()
        table.field_names = ['STR', 'CON', 'POW', 'DEX', 'APP', 'SIZ', 'INT', 'EDU']
        table.add_row([self.STR, self.CON, self.POW, self.DEX, self.APP, self.SIZ, self.INT, self.EDU])
        basic_status = table.get_string()

        return (f"{self.name}\n"
                f"SAN値: {self.SAN_LEFT}/{self.SAN_MAX}\n"
                '\n'
                f"{mutable_status}\n"
                '\n'
                f"{basic_status}\n")
