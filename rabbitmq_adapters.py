from kombu import Connection, Exchange, Producer, Queue, Consumer
from typing import Type, Any


def create_connection(rabbit_url: str, *args, **kwargs) -> Type[Connection]:
    return Connection(rabbit_url, *args, **kwargs)


def create_channel(conn: Type[Connection]) -> Any:
    return conn.channel()


def create_exchange(name: str, type: str) -> Type[Exchange]:
    return Exchange("example-exchange", type="direct")


def create_producer(exchange: Type[Exchange], channel: Any,
                    routing_key: str) -> Type[Producer]:
    return Producer(exchange=exchange, channel=channel, routing_key=routing_key)


def create_queue(name: str, exchange: Type[Exchange], routing_key: str) -> Type[Queue]:
    return Queue(name=name, exchange=exchange, routing_key=routing_key)


def create_consumer(conn: Type[Connection], queues: Type[Queue],
                    callbacks: list, accept: list) -> Type[Consumer]:
    return Consumer(conn, queues=queues, callbacks=callbacks, accept=accept)
