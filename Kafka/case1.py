import os
import click
from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv

load_dotenv()

bootstrap_server = os.getenv("bootstrap_server")


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("❌ Message delivery failed: {}".format(err))
    else:
        print(
            '✅  📬  Message delivered: "{}" to {} [partition {}]'.format(
                msg.value().decode("utf-8"), msg.topic(), msg.partition()
            )
        )


@click.command()
@click.option("--id", default="py_001", help="consumer_id")
@click.option("--producer_topic", default="topic2", help="producer topic")
@click.option("--consumer_topic", default="topic1", help="consumer topic")
def main(id, producer_topic, consumer_topic):
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
    consumer.subscribe([consumer_topic])

    # initialize producer
    producer = Producer({"bootstrap.servers": bootstrap_server})

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

            msg_plaintext = msg.value().decode("utf-8")
            print(
                '✅  📬  Message received: "{}" to {} [partition {}]'.format(
                    msg_plaintext, msg.topic(), msg.partition()
                )
            )

            producer.poll(0)
            data = f"message:{msg_plaintext}, topic:{msg.topic()}, partition:{msg.partition()}"
            producer.produce(
                producer_topic,
                key="key",
                value=data.encode("utf-8"),
                callback=delivery_report,
            )
    except:
        consumer.close()


if __name__ == "__main__":
    main()
