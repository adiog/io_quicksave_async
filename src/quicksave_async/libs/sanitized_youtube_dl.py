# This file is a part of [[$]] project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@brainfuck.pl>.
import re
import subprocess

from quicksave_async.util.regex import retrieve_from_string_by_regex


def sanitized_youtube_dl(video_url):
    download_command = 'youtube-dl %s' % video_url
    subprocess.check_call(download_command, shell=True)
    filename_command = 'youtube-dl --get-filename %s' % video_url
    original_filename = re.sub(r'\n', '', subprocess.check_output(filename_command.split(' ')).decode())
    sanitized_filename = sanitize_filename(original_filename)
    original_filepath = original_filename
    return original_filepath, sanitized_filename


def sanitize_filename(original_filename):
    return re.sub(r'[^a-zA-Z0-9\ _\-\.]', '_', original_filename)