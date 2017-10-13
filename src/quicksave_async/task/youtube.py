# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import subprocess

import os

import re
from generated.QsBeans import FileBean, DatabaseTaskBean, TagBean
from util.regex import retrieve_from_string_by_regex


def youtube(internalCreateRequest, storageProvider):
    meta = internalCreateRequest.createRequest.meta
    item_dir = storageProvider.getMetaPath(meta.meta_hash)
    video_file = item_dir + '/%(title)s'
    youtube_link = item_dir + '/youtube'
    youtube_dl_output = subprocess.check_output('youtube-dl --output \'%s\' %s' % (video_file, meta.source_url), shell=True).decode()
    output_file = retrieve_from_string_by_regex(youtube_dl_output, r'Merging formats into "(.*)"')
    subprocess.check_output(['ln', '-s', output_file, youtube_link])
    print(output_file)
    filesize = os.path.getsize(output_file)
    filename = re.sub(r'.*/', '', output_file)
    extension = re.sub(r'.*\.', '', filename)
    fileBean = FileBean(filename=filename, meta_hash=meta.meta_hash, mimetype='video/' + extension, filesize=filesize)
    tagBean = TagBean(meta_hash=meta.meta_hash, user_hash=meta.user_hash, name='youtube')
    meta.meta_type = 'quicksave/video'
    return [DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='insert', beanname='File', beanjson=fileBean.to_string()),
            DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='insert', beanname='Tag', beanjson=tagBean.to_string()),
            DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]
