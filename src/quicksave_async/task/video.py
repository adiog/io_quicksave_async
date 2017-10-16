# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import os
import re
import subprocess

import magic

from quicksave_pybeans.generated.QsBeans import FileBean, DatabaseTaskBean


def video(internal_create_request_bean, storage_provider):
    try:
        meta = internal_create_request_bean.createRequest.meta
        item_dir = storage_provider.getMetaPath(meta.meta_hash)
        run = subprocess.run(['wget', '--no-verbose', '--no-check-certificate', '-P', item_dir, meta.text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = run.stderr
        meta.text = ''
        output_file = re.sub(r'.*-> "([^"]*)".*', r'\1', output.decode(), flags=re.DOTALL)
        filesize = os.path.getsize(output_file)
        filename = re.sub(r'.*/', '', output_file)
        mimetype = magic.from_file(output_file, mime=True)
        file_bean = FileBean(filename=filename, meta_hash=meta.meta_hash, mimetype=mimetype, filesize=filesize)
        meta.meta_type = 'quicksave/video'
        return [DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='insert', beanname='File', beanjson=file_bean.to_string()),
                DatabaseTaskBean(databaseConnectionString=internal_create_request_bean.databaseConnectionString, type='update', beanname='Meta', beanjson=meta.to_string())]
    except:
        return []

