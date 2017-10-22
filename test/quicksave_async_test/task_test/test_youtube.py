# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.
import unittest

import os
from quicksave_pybeans.generated.QsBeans import InternalCreateRequestBean, CreateRequestBean, MetaBean

from quicksave_async.task.facebook import facebook_video
from quicksave_async.util.storage import LocalStorage


class youtube_test(unittest.TestCase):
    def test_youtube_video(self):
        meta_bean = MetaBean(
            meta_hash = 'abcdefgh',
            name = 'name',
            text = 'https://www.youtube.com/watch?v=WeEWhbn55Hc'
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

        self.assertNotEqual(facebook_video(internal_create_request_bean, storage_provider), [])
