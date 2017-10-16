# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import quicksave_async.env


def rabbit_push(channel, bean):
    channel.basic_publish(exchange='',
                          routing_key=quicksave_async.env.RESPONSE_QUEUE,
                          body=bean.to_string().encode())
