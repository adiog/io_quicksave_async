# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import re
import subprocess


def download_single_file(item_dir, item_url):
    run = subprocess.run(['wget', '--no-verbose', '--no-check-certificate', '-P', item_dir, item_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = run.stderr
    output_file = re.sub(r'.*-> "([^"]*)".*', r'\1', output.decode(), flags=re.DOTALL)
    return output_file

