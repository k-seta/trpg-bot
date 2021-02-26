#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

class CommandInterpreterLogic():

  def match_const(command):
    res = re.search('(\d+)', command)
    if res:
      return True, (int(res[0]),)
    else:
      return False, (0,)

  def match_ndn(command):
    res = re.search('(\d+)d(\d+)', command)
    if res:
      return True, tuple(map(int, res.groups()))
    else:
      return False, (0, 0)
  
  def match_d66(command):
    res = re.search('(d66)', command)
    if res:
      return True, res.groups()
    else:
      return False, (None, None)
  
  def tokenize_dices(self, command):
    return re.findall('(/|[\+\-<>]|\d+d\d+|\d+|d\d+|[^\s\+\-<>\d]+\d?)', command)[1:]

  def interp_command(self, command):

    if command.startswith('/ping'):
      return 'ping', ()

    if command.startswith('/debug'):
      return 'debug', ()
    
    if command.startswith('/redis'):
      return 'redis', ()

    if command.startswith('/sync'):
      return 'sync', ()

    if command.startswith('/help'):
      return 'help', ()

    if command.startswith('/status'):
      return 'status', ()

    if command.startswith('/players'):
      return 'players', ()

    match_mode = re.match('^/mode (.*)', command)
    if match_mode:
      return  'mode', match_mode.groups()

    match_regist = re.match('^/regist (http.*)', command)
    if match_regist:
      return 'regist', match_regist.groups()

    match_dice = re.match('^(/d\d+.*|/\d+d\d+.*)', command)
    if match_dice:
      return 'dice', self.tokenize_dices(command)
    
    if command.startswith('/'):
      return 'extra', (command)

    return '', None
