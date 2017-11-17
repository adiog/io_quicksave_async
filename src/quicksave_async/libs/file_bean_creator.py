# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import os

import magic
from quicksave_pybeans.generated.QsBeans import FileBean


def create_file_bean(meta, original_filepath, sanitized_filename):
    filesize = os.path.getsize(original_filepath)
    filename = sanitized_filename
    mimetype = magic.from_file(original_filepath, mime=True)
    file_bean = FileBean(filename=filename, meta_hash=meta.meta_hash, mimetype=mimetype, filesize=filesize)
    return file_bean