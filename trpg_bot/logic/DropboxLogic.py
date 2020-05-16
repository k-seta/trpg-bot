#!/usr/bin/env python
#-*- coding:utf-8 -*-

import shutil
import os
import dropbox

class DropboxLogic:

    def __init__(self, token):
        self.dbx = dropbox.Dropbox(token) 

    def sync(self):
        target_dir = './trpg_bot/resources/mayokin'
        if(os.path.exists(target_dir)):
            shutil.rmtree(target_dir)
        os.mkdir(target_dir)
        entries = self.dbx.files_list_folder('/mayokin').entries
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                self.dbx.files_download_to_file(f"{target_dir}/{entry.name}", entry.path_lower)
                print(f"downloaded {entry.path_lower}")
