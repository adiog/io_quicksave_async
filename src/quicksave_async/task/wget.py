# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import subprocess


def wget(internal_create_request_bean, storage_provider):
    try:
        meta = internal_create_request_bean.createRequest.meta
        item_dir = storage_provider.getMetaPath(meta.meta_hash)
        sitedump = item_dir + '/sitedump'
        subprocess.check_output(['wget', '--no-check-certificate', '-k', '-r', '-l', '1', '-p', '-P', sitedump, meta.source_url])
        subprocess.check_output(['tar', '-cvf', sitedump + '.tar', sitedump])
    except:
        pass
    return []
