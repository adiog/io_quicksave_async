# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import unittest

import os
from quicksave_pybeans.generated.QsBeans import InternalCreateRequestBean, CreateRequestBean, MetaBean

from quicksave_async.task.image import image
from quicksave_async.util.storage import LocalStorage


class image_test(unittest.TestCase):
    def test_image(self):
        meta_bean = MetaBean(
            meta_hash = 'abcdefgh',
            name = 'name',
            text = 'http://singervehicledesign.com/wp-content/uploads/2015/11/20-singer-911-manchester.jpg'
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

        self.assertNotEqual(image(internal_create_request_bean, storage_provider), [])
