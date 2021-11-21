#!/usr/bin/env python
import config as cfg
import threading, time

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
broker_list = cfg.kafka_brokers_available

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=broker_list)

        while not self.stop_event.is_set():
            producer.send(cfg.topic_name, b"test")
            producer.send(cfg.topic_name, b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=broker_list,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000, 
                                 group_id=cfg.consumer_group_1)
        consumer.subscribe([cfg.topic_name])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

        consumer.close()

class Consumer2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=broker_list,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000, 
                                 group_id=cfg.consumer_group_2)
        consumer.subscribe([cfg.topic_name])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

        consumer.close()


class Consumer3(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=broker_list,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000, 
                                 group_id=cfg.consumer_group_3)
        consumer.subscribe([cfg.topic_name])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

        consumer.close()


def main():
    #Create 'arjun-topic' Kafka topic
    try:
        admin = KafkaAdminClient(bootstrap_servers=broker_list)

        topic = NewTopic(name=cfg.topic_name,
                         num_partitions=9,
                         replication_factor=3)
        admin.create_topics([topic])
    except Exception:
        pass

    tasks = [
        Producer(),
        Consumer(),
        Consumer2(),
        Consumer3()
    ]

    # Start threads of a publisher/producer and a subscriber/consumer to 'arjun-topic' Kafka topic
    for t in tasks:
        t.start()

    time.sleep(10)

    # Stop threads
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
