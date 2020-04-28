#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

class Player:

    user = 'user'
    url = 'url'

    name = 'name'

    HP = '0'
    MP = '0'
    SAN_MAX = '0'
    IDA = '0'
    LUK = '0'
    ACK = '0'


    STR = '0'
    CON = '0'
    POW = '0'
    DEX = '0'
    APP = '0'
    SIZ = '0'
    INT = '0' 
    EDU = '0'

    battle_arts = {}
    find_arts = {}
    act_arts = {}
    commu_arts = {}
    know_arts = {}

    def __init__(self, user, url):
        self.user = user
        self.url = url

        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')

        self.name = soup.find('input', {'name': 'pc_name'})['value']

        self.HP = soup.find('input', {'name': 'NP9'})['value']
        self.MP = soup.find('input', {'name': 'NP10'})['value']
        self.SAN_LEFT = soup.find('input', {'name': 'SAN_Left'})['value']
        self.SAN_MAX = soup.find('input', {'name': 'NP11'})['value']
        self.IDA = soup.find('input', {'name': 'NP12'})['value']
        self.LUK = soup.find('input', {'name': 'NP13'})['value']
        self.ACK = soup.find('input', {'name': 'NP14'})['value']

        self.STR = soup.find('input', {'name': 'NP1'})['value']
        self.CON = soup.find('input', {'name': 'NP2'})['value']
        self.POW = soup.find('input', {'name': 'NP3'})['value']
        self.DEX = soup.find('input', {'name': 'NP4'})['value']
        self.APP = soup.find('input', {'name': 'NP5'})['value']
        self.SIZ = soup.find('input', {'name': 'NP6'})['value']
        self.INT = soup.find('input', {'name': 'NP7'})['value']
        self.EDU = soup.find('input', {'name': 'NP8'})['value']

        self.battle_arts = self.extract_table(soup, 'Table_battle_arts', 'TBAP[]')
        self.find_arts = self.extract_table(soup, 'Table_find_arts', 'TFAP[]')
        self.act_arts = self.extract_table(soup, 'Table_act_arts', 'TAAP[]')
        self.commu_arts = self.extract_table(soup, 'Table_commu_arts', 'TCAP[]')
        self.know_arts = self.extract_table(soup, 'Table_know_arts', 'TKAP[]')

    def extract_table(self, soup, table_id, value_name):
        keys = [key.text if key.text != '' else 'その他' for key in soup.find('table', {'id': table_id}).find_all('th',{})[8:]]
        values = [value['value'] for value in soup.find('table', {'id': table_id}).find_all('input', {'name': value_name})]
        return dict(zip(keys, values))

    def print(self):
        table = PrettyTable()
        table.field_names = ['HP', 'MP', 'IDA', 'LUK', 'ACK']
        table.add_row([self.HP, self.MP, self.IDA, self.LUK, self.ACK])
        mutable_status = table.get_string()

        table = PrettyTable()
        table.field_names = ['STR', 'CON', 'POW', 'DEX', 'APP', 'SIZ', 'INT', 'EDU']
        table.add_row([self.STR, self.CON, self.POW, self.DEX, self.APP, self.SIZ, self.INT, self.EDU])
        basic_status = table.get_string()

        battle_status = ''
        for key, value in self.battle_arts.items():
            battle_status += f"{key}: {value}\n"

        find_status = ''
        for key, value in self.find_arts.items():
            find_status += f"{key}: {value}\n"

        act_status = ''
        for key, value in self.act_arts.items():
            act_status += f"{key}: {value}\n"

        commu_status = ''
        for key, value in self.commu_arts.items():
            commu_status += f"{key}: {value}\n"

        know_status = ''
        for key, value in self.know_arts.items():
            know_status += f"{key}: {value}\n"

        return (f"{self.name}\n\n"
                "【能力値】\n"
                f"SAN値: {self.SAN_LEFT}/{self.SAN_MAX}"
                '\n'
                f"{mutable_status}\n"
                '\n'
                f"{basic_status}\n"
                '\n'
                '【戦闘技能】\n'
                f"{battle_status}\n"
                '【探索技能】\n'
                f"{find_status}\n"
                '【行動技能】\n'
                f"{act_status}\n"
                '【交渉技能】\n'
                f"{commu_status}\n"
                '【知識技能】\n'
                f"{know_status}\n")
