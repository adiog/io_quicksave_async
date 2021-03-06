# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import traceback

import sys

from quicksave_pybeans.generated.QsBeans import FileBean, DatabaseTaskBean, TagBean

from quicksave_async.libs.file_bean_creator import create_file_bean
from quicksave_async.libs.sanitized_youtube_dl import sanitized_youtube_dl


def youtube_video(internal_create_request_bean, storage_provider):
    try:
        meta = internal_create_request_bean.createRequest.meta

        video_url = meta.source_url

        original_filepath, sanitized_filename = sanitized_youtube_dl(video_url)
        file_bean = create_file_bean(meta, original_filepath, sanitized_filename)
        storage_provider.store(meta, original_filepath, sanitized_filename)

        tag_bean = TagBean(meta_hash=meta.meta_hash, user_hash=meta.user_hash, name='youtube-video')

        meta.meta_type = 'quicksave/video'

        return [DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='File', beanjson=file_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='Tag', beanjson=tag_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]
    except:
        print()
        traceback.print_exc(file=sys.stdout)
        print()
        return []
