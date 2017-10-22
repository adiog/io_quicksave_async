# This file is a part of [[$]] project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@brainfuck.pl>.
import re
import subprocess

import os

from quicksave_async.util.regex import retrieve_from_string_by_regex


def sanitized_youtube_dl(video_url):
    for ext in ['webm', 'mkv', 'mp4']:
        try:
            print(ext)
            return sanitized_youtube_dl_with_format(video_url, ext)
        except subprocess.CalledProcessError:
            pass
    raise RuntimeError()


def sanitized_youtube_dl_with_format(video_url, ext):
    filename_command = f'youtube-dl -f {ext} --merge-output-format {ext} --restrict-filenames --get-filename {video_url}'
    filename_command_output = subprocess.check_output(filename_command.split(' '))
    original_filename = re.sub(r'\n', '', filename_command_output.decode())
    download_command = f'youtube-dl -f {ext} --merge-output-format {ext} --restrict-filenames {video_url}'
    subprocess.check_call(download_command.split(' '))
    sanitized_filename = sanitize_filename(original_filename)
    original_filepath = original_filename
    return original_filepath, sanitized_filename


def sanitize_filename(original_filename):
    return re.sub(r'[^a-zA-Z0-9\ _\-\.]', '_', original_filename)