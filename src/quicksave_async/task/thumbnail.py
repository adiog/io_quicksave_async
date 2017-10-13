# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.
import os

from generated.QsBeans import DatabaseTaskBean, FileBean
from libs.crop_image import crop_image
from libs.selenium_thumbnail import save_thumbnail


def thumbnail(internalCreateRequest, storageProvider):
    meta = internalCreateRequest.createRequest.meta
    item_dir = storageProvider.getMetaPath(meta.meta_hash)
    thumbnail_file = item_dir + '/' + 'thumbnail.png'
    thumbnail_crop = item_dir + '/' + 'thumbnail_crop.png'
    save_thumbnail(url=meta.source_url, thumbnail_file=thumbnail_file)
    crop_image(thumbnail_file, thumbnail_crop)
    filesize = os.path.getsize(thumbnail_crop)
    fileBean = FileBean(filename='thumbnail_crop.png', meta_hash=meta.meta_hash, mimetype='image/png', filesize=filesize)
    return [DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='insert', beanname='File', beanjson=fileBean.to_string())]
