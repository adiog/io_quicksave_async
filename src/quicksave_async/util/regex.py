# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import re


def retrieve_from_string_by_regex(text, regex):
    match = re.search(regex, text, flags=(re.DOTALL | re.IGNORECASE))
    if match:
        return match.group(1)
    else:
        return ''
