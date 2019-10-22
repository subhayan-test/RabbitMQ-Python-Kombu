from time import sleep
from rabbitmq_adapters import *


rabbit_url = "amqp://localhost:5672/"

conn = create_connection(rabbit_url)
channel = create_channel(conn)

exchange = create_exchange("example-exchange", type="direct")

producer = create_producer(
    exchange=exchange, channel=channel, routing_key="BOB")

queue = create_queue(name="example-queue",
                     exchange=exchange, routing_key="BOB")

queue.maybe_bind(conn)
queue.declare()


producer.publish("END OF MESSAGE..")
