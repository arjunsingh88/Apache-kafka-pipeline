# from kafka import KafkaConsumer
# consumer = KafkaConsumer('arjun-topic', group_id='my_favorite_group', bootstrap_servers=['localhost:9092','localhost:9094','localhost:9095'])
# for msg in consumer:
#      print (msg)
import threading, time
import pandas as pd

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

class Consumer(threading.Thread):
    def __init__(self, brokers, consumer_group, topic_name):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.broker_list = brokers
        self.consumer_group = consumer_group
        self.topic = topic_name

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker_list,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000, 
                                 group_id=self.consumer_group)
        consumer.subscribe([self.topic])
        li = []
        keys = ['consumer_group', 'data']
        di = dict.fromkeys(keys, None)
        while not self.stop_event.is_set():
            for message in consumer:
                print(self.consumer_group, message)
                # data = message.value
                # Storing data into dataframe
                # print(data)
                # di['consumer_group'] = self.consumer_group
                # di['data'] = data
                # li.append(di)
                if self.stop_event.is_set():
                    break
        
        # metrics = consumer.metrics()
        # print(pd.DataFrame(li))
        consumer.close()