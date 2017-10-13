# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import subprocess


def wget(internalCreateRequest, storageProvider):
    meta = internalCreateRequest.createRequest.meta
    item_dir = storageProvider.getMetaPath(meta.meta_hash)
    sitedump = item_dir + '/sitedump'
    subprocess.check_output(['wget', '--no-check-certificate', '-k', '-P', sitedump, meta.source_url])
    subprocess.check_output(['tar', '-cvf', sitedump + '.tar', sitedump])
    return []
