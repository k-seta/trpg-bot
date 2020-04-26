#!/usr/bin/env python
#-*- coding:utf-8 -*-

class Player:
    user = 'discord account name'
    url = 'profile url'

    def __init__(self, user, url):
        this.user = user
        this.url = url

    def __str__(self):
        return f"{this.user}: {this.url}"

    def to_dict(self):
        return {'user': this.user, 'url', this.url}
