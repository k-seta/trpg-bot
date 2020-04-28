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
