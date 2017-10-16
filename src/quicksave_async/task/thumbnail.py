# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.
import os

from quicksave_pybeans.generated.QsBeans import DatabaseTaskBean, FileBean
from quicksave_async.libs.crop_image import crop_image
from quicksave_async.libs.selenium_thumbnail import save_thumbnail


def thumbnail(internal_create_request_bean, storage_provider):
    try:
        meta = internal_create_request_bean.createRequest.meta
        item_dir = storage_provider.getMetaPath(meta.meta_hash)
        thumbnail_file = item_dir + '/' + 'thumbnail.png'
        thumbnail_crop = item_dir + '/' + 'thumbnail_crop.png'
        save_thumbnail(url=meta.source_url, thumbnail_file=thumbnail_file)
        crop_image(thumbnail_file, thumbnail_crop)
        filesize = os.path.getsize(thumbnail_crop)
        file_bean = FileBean(filename='thumbnail_crop.png', meta_hash=meta.meta_hash, mimetype='image/png', filesize=filesize)
        return [DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='File', beanjson=file_bean.to_string())]
    except:
        pass
