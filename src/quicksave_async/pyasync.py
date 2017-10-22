# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.
import traceback

import sys

from quicksave_async.rabbit_loop import rabbit_loop
from quicksave_async.rabbit_push import rabbit_push
from quicksave_async.task.audio import audio
from quicksave_async.task.facebook import facebook_video
from quicksave_async.task.git import git
from quicksave_async.task.image import image
from quicksave_async.task.neingag import neingag
from quicksave_async.task.thumbnail import thumbnail
from quicksave_async.task.video import video
from quicksave_async.task.wget import wget
from quicksave_async.task.youtube import youtube_video
from quicksave_async.util.logger import log
from quicksave_async.util.storage import Sshfs, StorageFactory
from quicksave_async.util.timer import Timer
from quicksave_pybeans.generated.QsBeans import MetaBean, BackgroundTaskBean, TagBean, DatabaseTaskBean


def task(name, internal_create_request_bean, params):
    meta = internal_create_request_bean.createRequest.meta

    storage = StorageFactory.create(internal_create_request_bean.storageConnectionString, meta.user_hash, internal_create_request_bean.keys)
    storage.init(meta.meta_hash)

    if name == 'git':
        return git(internal_create_request_bean, storage)
    elif name == 'audio':
        return audio(internal_create_request_bean, storage)
    elif name == 'video':
        return video(internal_create_request_bean, storage)
    elif name == 'image':
        return image(internal_create_request_bean, storage)
    elif name == 'thumbnail':
        return thumbnail(internal_create_request_bean, storage)
    elif name == '9gag':
        return neingag(internal_create_request_bean, storage)
    elif name == 'wget':
        return wget(internal_create_request_bean, storage)
    elif name == 'youtube:video':
        return youtube_video(internal_create_request_bean, storage)
    elif name == 'facebook:video':
        return facebook_video(internal_create_request_bean, storage)
    else:
        log('WARNING: Unsupported task type: <%s>' % name)
        return []


def task_callback(channel, task_bean):
    with Timer('%s' % task_bean.name):
        try:
            database_tasks = task(task_bean.name, task_bean.internalCreateRequest, task_bean.kwargs)
            for database_task in database_tasks:
                rabbit_push(channel, database_task)
            meta = task_bean.internalCreateRequest.createRequest.meta
            tag_bean = TagBean(meta_hash=meta.meta_hash, user_hash=meta.user_hash, name='python_async:{}'.format(task_bean.name))
            database_task = DatabaseTaskBean(databaseConnectionString=task_bean.internalCreateRequest.databaseConnectionString, type='insert', beanname='Tag', beanjson=tag_bean.to_string())
            rabbit_push(channel, database_task)
        except:
            print()
            traceback.print_exc(file=sys.stdout)
            print()
            log('ERROR processing bean:')
            log(task_bean.to_string())


def main():
    rabbit_loop(BackgroundTaskBean, task_callback)


if __name__ == '__main__':
    main()
