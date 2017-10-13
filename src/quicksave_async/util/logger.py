# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import datetime


def log(message=''):
    print(datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S] ") + message)