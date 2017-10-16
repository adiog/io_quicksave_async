# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import json

import pika

import quicksave_async.env


def rabbit_loop(bean, bean_callback):
    def consume_callback(channel, method, properties, body):
        bean_callback(channel, bean(json.loads(body.decode())))

    connection_parameters = pika.ConnectionParameters(host=quicksave_async.env.IO_QUICKSAVE_MQ_HOST,
                                                      port=quicksave_async.env.IO_QUICKSAVE_MQ_PORT)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue=quicksave_async.env.REQUEST_QUEUE)
    channel.queue_declare(queue=quicksave_async.env.RESPONSE_QUEUE)
    channel.basic_consume(consume_callback,
                          queue=quicksave_async.env.REQUEST_QUEUE,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()
