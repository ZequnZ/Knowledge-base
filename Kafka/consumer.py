import os
import click
from confluent_kafka import Consumer
from dotenv import load_dotenv

load_dotenv()

bootstrap_server = os.getenv("bootstrap_server")
topic = os.getenv("topic")
# group_id = 'py_001'


@click.command()
@click.option("--id", default="py_001", help="consumer_id")
def create_consumer(id):
    print(id)
    print(bootstrap_server)
    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_server,
            "group.id": id,
            "enable.auto.commit": "true",
            "session.timeout.ms": 6000,
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([topic])
    print("Start...")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # print("Message: {None}")
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            print(
                '✅  📬  Message received: "{}" to {} [partition {}]'.format(
                    msg.value().decode("utf-8"), msg.topic(), msg.partition()
                )
            )
    except:
        consumer.close()
    return consumer


if __name__ == "__main__":
    consumer = create_consumer()
    # print(consumer)
    # print('Start...')
