# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import os
import re
import subprocess

from quicksave_async.util.regex import retrieve_from_string_by_regex
from quicksave_pybeans.generated.QsBeans import FileBean, DatabaseTaskBean, TagBean


def facebook_video(internal_create_request_bean, storage_provider):
    try:
        meta = internal_create_request_bean.createRequest.meta
        item_dir = storage_provider.getMetaPath(meta.meta_hash)
        video_file = item_dir + '/%(title)s'
        facebook_link = item_dir + '/facebook-video'
        youtube_dl_output = subprocess.check_output('youtube-dl --output \'%s\' %s' % (video_file, meta.text), shell=True).decode()
        output_file = retrieve_from_string_by_regex(youtube_dl_output, r'Merging formats into "(.*)"')
        subprocess.check_output(['ln', '-s', output_file, facebook_link])
        print(output_file)
        filesize = os.path.getsize(output_file)
        filename = re.sub(r'.*/', '', output_file)
        extension = re.sub(r'.*\.', '', filename)
        file_bean = FileBean(filename=filename, meta_hash=meta.meta_hash, mimetype='video/' + extension, filesize=filesize)
        tagBean = TagBean(meta_hash=meta.meta_hash, user_hash=meta.user_hash, name='facebook-video')
        meta.meta_type = 'quicksave/video'
        return [DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='File', beanjson=file_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='Tag', beanjson=tagBean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]
    except:
        return []
