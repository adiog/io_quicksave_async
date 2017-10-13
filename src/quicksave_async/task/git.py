# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import subprocess
import tempfile
import re


def git(internalCreateRequest, storageProvider):
    meta = internalCreateRequest.createRequest.meta
    tmp = tempfile.mkdtemp()
    source = tmp + '/' + 'git'
    repo_url = re.sub(r'/$', '', meta.source_url)
    subprocess.check_output(['git', 'clone', repo_url, source])
    subprocess.check_output(['tar', '-cvf', source + '.tar', source])
    item_dir = storageProvider.getMetaPath(meta.meta_hash)
    target = item_dir + '/git'
    storageProvider.move(source, target)
    storageProvider.move(source + '.tar', target + '.tar')
    return []

