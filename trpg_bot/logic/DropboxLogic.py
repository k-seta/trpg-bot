#!/usr/bin/env python
#-*- coding:utf-8 -*-

import dropbox

class DropboxLogic:

    def __init__(self, token):
        self.dbx = dropbox.Dropbox(token) 

    def sync(self):
        entries = self.dbx.files_list_folder('/mayokin').entries
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                self.dbx.files_download_to_file(f"./trpg_bot/resources/mayokin/{entry.name}", entry.path_lower)
                print(f"downloaded {entry.path_lower}")
