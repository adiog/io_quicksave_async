# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import requests
from bs4 import BeautifulSoup


def picker(url, selector):
    response = requests.get(url)
    html_content = response.text
    soup_document = BeautifulSoup(html_content)
    return soup_document.select(selector)
