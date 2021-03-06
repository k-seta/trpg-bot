#!/usr/bin/env python
#-*- coding:utf-8 -*-

import shutil
import os
import dropbox
import zipfile

class DropboxLogic:

    def __init__(self, token):
        self.dbx = dropbox.Dropbox(token) 
    
    def sync(self):
        target_dir = './trpg_bot/resources'
        if(os.path.exists(f"{target_dir}/mayokin")):
            shutil.rmtree(f"{target_dir}/mayokin")
        zip_path = f"{target_dir}/dice_lists.zip"
        self.dbx.files_download_zip_to_file(zip_path, '/mayokin')
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(target_dir)
        os.remove(zip_path)
        print('downloaded txt files.')

