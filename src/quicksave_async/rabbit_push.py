import pika
import env

def rabbit_push(queue, bean):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=env.IO_QUICKSAVE_MQ_HOST, port=env.IO_QUICKSAVE_MQ_PORT))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=bean.to_string().encode())
    connection.close()