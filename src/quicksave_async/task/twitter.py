# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import subprocess
import traceback

import sys

from quicksave_pybeans.generated.QsBeans import FileBean, DatabaseTaskBean, TagBean

from quicksave_async.libs.file_bean_creator import create_file_bean
from quicksave_async.libs.sanitized_youtube_dl import sanitized_youtube_dl


def twitter_tweet(internal_create_request_bean, storage_provider):
    meta = internal_create_request_bean.createRequest.meta

    twitter_url = meta.source_url

    try:
        item_dir = storage_provider.getMetaPath(meta.meta_hash)
        twitterdump = item_dir + '/twitterdump'
        subprocess.check_output(['wget', '--no-check-certificate', '-e', 'robots=off', '-P', twitterdump,
                                 '-k', '-p', '--span-hosts', '--domains', 'twitter.com,abs.twimg.com,pbs.twimg.com,twimg.com',
                                 twitter_url])
    except:
        pass

    try:
        original_filepath, sanitized_filename = sanitized_youtube_dl(twitter_url)
        file_bean = create_file_bean(meta, original_filepath, sanitized_filename)
        storage_provider.store(meta, original_filepath, sanitized_filename)

        tag_bean = TagBean(meta_hash=meta.meta_hash, user_hash=meta.user_hash, name='twitter')

        meta.meta_type = 'quicksave/tweet'

        return [DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='File', beanjson=file_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='Tag', beanjson=tag_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]
    except:
        print()
        traceback.print_exc(file=sys.stdout)
        print()
        return []
