# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.
import unittest

import os
from quicksave_pybeans.generated.QsBeans import InternalCreateRequestBean, CreateRequestBean, MetaBean

from quicksave_async.task.twitter import twitter_tweet
from quicksave_async.task.youtube import youtube_video
from quicksave_async.util.storage import LocalStorage


class twitter_test(unittest.TestCase):
    def test_twitter_tweet(self):
        meta_bean = MetaBean(
            meta_hash = 'abcdefgh',
            name = 'name',
            source_url = 'https://twitter.com/gringogidget/status/931185432057937920'
        )
        create_request_bean = CreateRequestBean(
            meta = meta_bean
        )
        internal_create_request_bean = InternalCreateRequestBean(
            createRequest = create_request_bean,
            keys = [],
            databaseConnectionString='',
            storageConnectionString=''
        )

        storage_provider = LocalStorage(os.getcwd())
        storage_provider.init(meta_bean.meta_hash)

        self.assertNotEqual(twitter_tweet(internal_create_request_bean, storage_provider), [])

    def test_twitter_tweet(self):
        meta_bean = MetaBean(
            meta_hash = 'axcdefgh',
            name = 'name',
            source_url = 'https://twitter.com/OnlineMagazin/status/912272171413762048'
        )
        create_request_bean = CreateRequestBean(
            meta = meta_bean
        )
        internal_create_request_bean = InternalCreateRequestBean(
            createRequest = create_request_bean,
            keys = [],
            databaseConnectionString='',
            storageConnectionString=''
        )

        storage_provider = LocalStorage(os.getcwd())
        storage_provider.init(meta_bean.meta_hash)

        self.assertNotEqual(twitter_tweet(internal_create_request_bean, storage_provider), [])

