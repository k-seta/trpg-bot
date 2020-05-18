#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

class CommandInterpreter():

  def parse(message):
    command = message.content

    if command[:5] == '/ping':
      return 'ping', None

    if command[:6] == '/debug':
      return 'debug', None
    
    if command[:6] == '/redis':
      return 'redis', None

    if command[:5] == '/sync':
      return 'sync', None

    if command[:5] == '/help':
      return 'help', None

    if command[:7] == '/status':
      return 'status', None

    if command[:8] == '/players':
      return 'players', None

    match_mode = re.match('^/mode (.*)', command)
    if match_mode:
      return  'mode', *match_mode.groups()

    match_regist = re.match('^/regist (http.*)', command)
    if match_regist:
      return 'regist', *match_regist.groups()

    match_dn = re.match('^/(d\d+.*)', command)
    if match_dn:
      return 'dn', *match_dn.groups()
    
    match_ndn = re.match('^/(\d+d\d+.*)', command)
    if match_ndn:
      return 'ndn', *match_ndn.groups()
    
    return '', None
