# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.
import re
import subprocess

from quicksave_pybeans.generated.QsBeans import DatabaseTaskBean

from quicksave_async.libs import soup_picker
from quicksave_async.libs.file_bean_creator import create_file_bean
from quicksave_async.libs.download_single_file import download_single_file


def neingag(internal_create_request_bean, storage_provider):
    try:
        meta = internal_create_request_bean.createRequest.meta

        gag_url = meta.text
        meta.text = ''

        item_dir = storage_provider.getMetaPath(meta.meta_hash)

        content_node = soup_picker.picker(gag_url, 'div.image-post > img')
        nein_source = content_node[0]['src']
        output_file = download_single_file(item_dir, nein_source)

        filename = re.sub(r'.*/', '', output_file)
        file_bean = create_file_bean(meta, output_file, filename)

        meta.meta_type = 'quicksave/image'
        return [DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='File', beanjson=file_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]
    except:
        pass
    return []
