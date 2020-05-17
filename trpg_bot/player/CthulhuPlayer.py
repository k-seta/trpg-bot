#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from player.AbstractPlayer import AbstractPlayer

class CthulhuPlayer(AbstractPlayer):

    user = 'user'
    url = 'url'

    name = 'name'

    status = {}
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

        HP = soup.find('input', {'name': 'NP9'})['value']
        MP = soup.find('input', {'name': 'NP10'})['value']
        IDA = soup.find('input', {'name': 'NP12'})['value']
        LUK = soup.find('input', {'name': 'NP13'})['value']
        ACK = soup.find('input', {'name': 'NP14'})['value']
        SAN_LEFT = soup.find('input', {'name': 'SAN_Left'})['value']
        SAN_MAX = soup.find('input', {'name': 'NP11'})['value']

        STR = soup.find('input', {'name': 'NP1'})['value']
        CON = soup.find('input', {'name': 'NP2'})['value']
        POW = soup.find('input', {'name': 'NP3'})['value']
        DEX = soup.find('input', {'name': 'NP4'})['value']
        APP = soup.find('input', {'name': 'NP5'})['value']
        SIZ = soup.find('input', {'name': 'NP6'})['value']
        INT = soup.find('input', {'name': 'NP7'})['value']
        EDU = soup.find('input', {'name': 'NP8'})['value']

        keys = ['HP', 'MP', 'IDA', 'LUK', 'ACK', 'SAN_LEFT', 'SAN_MAX', 'STR', 'CON', 'POW', 'DEX', 'APP', 'SIZ', 'INT', 'EDU']
        values = [HP, MP, IDA, LUK, ACK, SAN_LEFT, SAN_MAX, STR, CON, POW, DEX, APP, SIZ, INT, EDU]
        self.status = dict(zip(keys, values))

        self.battle_arts = self.extract_table(soup, 'Table_battle_arts', 'TBAP[]')
        self.find_arts = self.extract_table(soup, 'Table_find_arts', 'TFAP[]')
        self.act_arts = self.extract_table(soup, 'Table_act_arts', 'TAAP[]')
        self.commu_arts = self.extract_table(soup, 'Table_commu_arts', 'TCAP[]')
        self.know_arts = self.extract_table(soup, 'Table_know_arts', 'TKAP[]')

    def extract_table(self, soup, table_id, value_name):
        elements = soup.find('table', {'id': table_id}).find_all('th',{})[8:]
        def el2text(el):
            if el.text == '':
                # 追加した技能名
                return el.find('input')['value'] if el.find('input')['value'] else 'その他'
            elif el.find('input'):
                # 技能名 + (詳細)
                return el.text[:-1] + el.find('input')['value'] + ')'
            else:
                # 技能名
                return el.text

        keys = list(map(el2text, elements))
        values = [value['value'] for value in soup.find('table', {'id': table_id}).find_all('input', {'name': value_name})]
        return dict(zip(keys, values))

    def get(self, param):
        if param == 'SAN':
            return self.status['SAN_LEFT']
        if param in self.status.keys():
            return self.status[param]
        if param in self.battle_arts.keys():
            return self.battle_arts[param]
        if param in self.find_arts.keys():
            return self.find_arts[param]
        if param in self.act_arts.keys():
            return self.act_arts[param]
        if param in self.commu_arts.keys():
            return self.commu_arts[param]
        if param in self.know_arts.keys():
            return self.know_arts[param]
        return ''

    def print(self):
        table = PrettyTable()
        table.field_names = list(self.status.keys())[:5]
        table.add_row(list(self.status.values())[:5])
        mutable_status = table.get_string()

        table = PrettyTable()
        table.field_names = list(self.status.keys())[7:]
        table.add_row(list(self.status.values())[7:])
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

        return (f"{self.name}\n"
                f"{self.url}\n\n"
                "【能力値】\n"
                f"SAN値: {self.status['SAN_LEFT']}/{self.status['SAN_MAX']}"
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
