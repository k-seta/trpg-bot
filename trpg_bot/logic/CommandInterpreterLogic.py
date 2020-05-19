#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

class CommandInterpreterLogic():

  def match_ndn(command):
    res = re.search('(\d+)d(\d+)', command)
    if res:
      return True, map(int, res.groups())
    else:
      return False, (0, 0)
  
  def match_const(command):
    res = re.search('(\d+)', command)
    if res:
      return True, (int(res[0]),)
    else:
      return False, (0,)
  
  def match_d66(command):
    res = re.search('/(d66) (.*)', command)
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

  def interp_command(message):
    command = message.content

    if '/ping' in command:
      return 'ping', None

    if '/debug' in command:
      return 'debug', None
    
    if '/redis' in command:
      return 'redis', None

    if '/sync' in command:
      return 'sync', None

    if '/help' in command:
      return 'help', None

    if '/status' in command:
      return 'status', None

    if '/players' in command:
      return 'players', None

    match_mode = re.match('^/mode (.*)', command)
    if match_mode:
      return  'mode', *match_mode.groups()

    match_regist = re.match('^/regist (http.*)', command)
    if match_regist:
      return 'regist', *match_regist.groups()

    match_dn = re.match('^/(d\d+ .*)', command)
    if match_dn:
      return 'dn', *match_dn.groups()
    
    match_ndn = re.match('^/(\d+d\d+.*)', command)
    if match_ndn:
      return 'ndn', *match_ndn.groups()
    
    return '', None
