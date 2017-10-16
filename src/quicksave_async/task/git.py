# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import subprocess
import tempfile

import os

import magic
from generated.QsBeans import FileBean, DatabaseTaskBean


def git(internalCreateRequest, storageProvider):
    try:
        meta = internalCreateRequest.createRequest.meta
        tmp = tempfile.mkdtemp()
        source = tmp + '/' + 'git'
        github_path = meta.source_url.split('github.com/')
        user_repo_rest_list = github_path[1].split('/')
        user = user_repo_rest_list[0]
        repo = user_repo_rest_list[1]
        repo_url = f'https://github.com/{user}/{repo}'
        subprocess.check_output(['git', 'clone', repo_url, source])
        subprocess.check_output(['tar', '-cvf', source + '.tar', source])
        item_dir = storageProvider.getMetaPath(meta.meta_hash)
        target = item_dir + '/git'
        storageProvider.move(source, target)
        target_tar = target + 'tar'
        storageProvider.move(source + '.tar', target_tar)

        filesize = os.path.getsize(target_tar)
        filename = 'git.tar'
        mimetype = magic.from_file(target_tar, mime=True)
        fileBean = FileBean(filename=filename, meta_hash=meta.meta_hash, mimetype=mimetype, filesize=filesize)
        meta.meta_type = 'quicksave/image'
        return [DatabaseTaskBean(databaseConnectionString=internalCreateRequest.databaseConnectionString, type='insert', beanname='File', beanjson=fileBean.to_string())]
    except:
        return []

