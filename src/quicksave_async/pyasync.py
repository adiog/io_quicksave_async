# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

from quicksave_pybeans.generated.QsBeans import MetaBean, BackgroundTaskBean, TagBean, DatabaseTaskBean
from quicksave_async.rabbit_poll import rabbit_poll
from quicksave_async.rabbit_push import rabbit_push
from quicksave_async.task.git import git
from quicksave_async.task.image import image
from quicksave_async.task.thumbnail import thumbnail
from quicksave_async.task.wget import wget
from quicksave_async.task.youtube import youtube
from quicksave_async.util.logger import log
from quicksave_async.util.storage import Sshfs, StorageFactory
from quicksave_async.util.timer import Timer


def task(name, internalCreateRequest, params):
    meta = internalCreateRequest.createRequest.meta

    storage = StorageFactory.create(internalCreateRequest.storageConnectionString, meta.user_hash, internalCreateRequest.keys)
    storage.init(meta.meta_hash)

    if name == 'git':
        return git(internalCreateRequest, storage)
    elif name == 'image':
        return image(internalCreateRequest, storage)
    elif name == 'thumbnail':
        return thumbnail(internalCreateRequest, storage)
    elif name == 'wget':
        return wget(internalCreateRequest, storage)
    elif name == 'youtube':
        return youtube(internalCreateRequest, storage)
    else:
        log('WARNING: Unsupported task type: <%s>' % name)
        return []


def task_callback(task_bean):
    with Timer('%s' % (task_bean.name)):
        #try:
            database_tasks = task(task_bean.name, task_bean.internalCreateRequest, task_bean.kwargs)
            for database_task in database_tasks:
                rabbit_push('response', database_task)
            meta = task_bean.internalCreateRequest.createRequest.meta
            tagBean = TagBean(meta_hash=meta.meta_hash, user_hash=meta.user_hash, name='python_async:{}'.format(task_bean.name))
            database_task = DatabaseTaskBean(databaseConnectionString=task_bean.internalCreateRequest.databaseConnectionString, type='insert', beanname='Tag', beanjson=tagBean.to_string())
            rabbit_push('response', database_task)
        #except:
        #    log('ERROR processing bean:')
        #    log(task_bean.to_string())

def main():
    rabbit_poll('request', BackgroundTaskBean, task_callback)


if __name__ == '__main__':
    main()
