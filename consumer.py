from rabbitmq_adapters import *
import socket
import sys

rabbit_url = "amqp://localhost:5672/"

conn = create_connection(rabbit_url, heartbeat=2)
exchange = create_exchange("example-exchange", type="direct")
queue = create_queue(name="example-queue",
                     exchange=exchange, routing_key="BOB")


def process_message(body, message):
    if not body == "END OF MESSAGE..":
        print(body)
        message.ack()
    else:
        message.ack()
        print("Closing message is sent ...should close the connection")
        sys.exit()


consumer = create_consumer(conn, queues=queue, callbacks=[
    process_message], accept=["text/plain"])
consumer.consume()


def establish_connection():
    revived_connection = conn.clone()
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    consumer.revive(channel)
    consumer.consume()
    return revived_connection


def consume():
    new_conn = establish_connection()
    while True:
        try:
            new_conn.drain_events(timeout=2)
        except socket.timeout:
            new_conn.heartbeat_check()


def run():
    while True:
        try:
            consume()
        except conn.connection_errors:
            print("connection revived")


if __name__ == "__main__":
    run()
