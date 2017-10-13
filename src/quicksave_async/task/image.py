# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import re
import subprocess

import os

import magic
from generated.QsBeans import FileBean, DatabaseTaskBean


def image(internalCreateRequest, storageProvider):
    meta = internalCreateRequest.createRequest.meta
    item_dir = storageProvider.getMetaPath(meta.meta_hash)
    print(meta.text)
    print('0')
    run = subprocess.run(['wget', '--no-check-certificate', '-P', item_dir, meta.text], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    print('1')
    output = run.stderr
    meta.text = ''
    print(output)
    print('2')
    output_file = re.sub(r'.*Saving to: ‘([^\n]*)’.*', r'\1', output.decode(), flags=re.DOTALL)
    print(output_file)
    print('3')
    filesize = os.path.getsize(output_file)
    filename = re.sub(r'.*/', '', output_file)
    mimetype = magic.from_file(output_file, mime=True)
    fileBean = FileBean(filename=filename, meta_hash=meta.meta_hash, mimetype=mimetype, filesize=filesize)
    meta.meta_type = 'quicksave/image'
    return [DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='insert', beanname='File', beanjson=fileBean.to_string()),
            DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]

