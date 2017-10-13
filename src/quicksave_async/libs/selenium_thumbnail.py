# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

from selenium import webdriver


def save_thumbnail(url, thumbnail_file):
    browser = webdriver.PhantomJS()
    browser.get(url)
    browser.save_screenshot(thumbnail_file)
    browser.quit()
