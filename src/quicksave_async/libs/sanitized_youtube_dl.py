# This file is a part of [[$]] project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@brainfuck.pl>.
import re
import subprocess

from quicksave_async.util.regex import retrieve_from_string_by_regex


def sanitized_youtube_dl(video_url):
    download_command = 'youtube-dl %s' % video_url
    download_command_output = subprocess.check_output(download_command, shell=True).decode()
    original_filename = retrieve_from_string_by_regex(download_command_output, r'Merging formats into "(.*)"')
    sanitized_filename = sanitize_filename(original_filename)
    original_filepath = './' + original_filename
    return original_filepath, sanitized_filename


def sanitize_filename(original_filename):
    return re.sub(r'[^a-zA-Z0-9\ _\-\.]', '_', original_filename)