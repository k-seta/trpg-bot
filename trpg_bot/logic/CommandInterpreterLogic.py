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
  
  def match_ndn_txt(command):
    res = re.search('(\d+d\d+) (.+)', command)
    if res:
      return True, res.groups()
    else:
      return False, (None, None)

  def match_d66_txt(command):
    res = re.search('/(d66) (.*)', command)
    if res:
      return True, res.groups()
    else:
      return False, (None, None)
  
  def tokenize_dices(command):
    return re.findall('(/|[\+<>]|\d+d\d+|\d+|d\d+|[^\s\+<>\d]+)', command)[1:]

  def interp_command(command):

    if '/ping' in command:
      return 'ping', ()

    if '/debug' in command:
      return 'debug', ()
    
    if '/redis' in command:
      return 'redis', ()

    if '/sync' in command:
      return 'sync', ()

    if '/help' in command:
      return 'help', ()

    if '/status' in command:
      return 'status', ()

    if '/players' in command:
      return 'players', ()

    match_mode = re.match('^/mode (.*)', command)
    if match_mode:
      return  'mode', match_mode.groups()

    match_regist = re.match('^/regist (http.*)', command)
    if match_regist:
      return 'regist', match_regist.groups()

    match_dice = re.match('^(/d\d+ .*|/\d+d\d+.*)', command)
    if match_dice:
      return 'dice', self.tokenize_dices(command)
    
    return '', None
