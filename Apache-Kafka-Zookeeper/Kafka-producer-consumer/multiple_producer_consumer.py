#!/usr/bin/env python
import config as cfg
import threading, time
from producer import Producer
from consumer import Consumer
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
import pandas as pd


#Additional info from config file
broker_list = cfg.kafka_brokers_available
topic_name = cfg.topic_name
consumer_group1 = cfg.consumer_group_1
consumer_group2 = cfg.consumer_group_2
consumer_group3 = cfg.consumer_group_3

def main():
    try:
        admin = KafkaAdminClient(bootstrap_servers=broker_list)

        topic = NewTopic(name=topic_name,
                         num_partitions=9,
                         replication_factor=3)
        admin.create_topics([topic])
    except Exception:
        pass
    
    #Create producer and consumer
    Producer_1 = Producer(broker_list, topic_name)
    Consumer_1 = Consumer(broker_list, consumer_group1, topic_name)
    Consumer_2 = Consumer(broker_list, consumer_group2, topic_name)
    Consumer_3 = Consumer(broker_list, consumer_group3, topic_name)

    #Start producer and consumer
    tasks = [
        Producer_1,
        Consumer_1,
        Consumer_2,
        Consumer_3
    ]

    # Start threads of a publisher/producer and a subscriber/consumer's to 'arjun-topic' Kafka topic
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