#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from player.AbstractPlayer import AbstractPlayer

class MayokinPlayer(AbstractPlayer):
  
  user = 'user'
  url = 'url'

  name = 'name'

  profile = {} #class, job
  status = {} 

  def __init__(self, user, url):
    self.user = user
    self.url = url

    res = requests.get(self.url)
    soup = BeautifulSoup(res.text, 'html.parser')

    self.name = soup.find('input', {'name': 'pc_name'})['value']

    status_section = soup.find('section', {'id': 'status_disp'})

    self.profile['レベル']  = soup.find('input', {'name': 'Level'})['value']
    self.profile['クラス']  = soup.find('input', {'name': 'class_name'})['value']
    self.profile['ジョブ1'] = soup.find('input', {'name': 'job1_name'})['value']
    self.profile['ジョブ2'] = soup.find('input', {'name': 'job2_name'})['value']

    self.status['才覚'] = soup.find('input', {'name': 'NP1'})['value']
    self.status['魅力'] = soup.find('input', {'name': 'NP2'})['value']
    self.status['探索'] = soup.find('input', {'name': 'NP3'})['value']
    self.status['武勇'] = soup.find('input', {'name': 'NP4'})['value']
    self.status['HP']   = soup.find('input', {'name': 'NP5'})['value']
    self.status['器']   = soup.find('input', {'name': 'NP6'})['value']
    self.status['回避'] = soup.find('input', {'name': 'NP7'})['value']
    self.status['配下'] = soup.find('input', {'name': 'NP8'})['value']


  def get(self, param):
    if param in self.status.keys():
      return self.status[param]

  def print(self):
    profile = ''
    for key, value in self.profile.items():
        profile += f"{key}: {value}\n"

    status = ''
    for key, value in self.status.items():
        status += f"{key}: {value}\n"

    return (f"{self.name}\n"
            f"{self.url}\n\n"
            f"{profile}\n"
            '\n'
            f"{status}\n")



