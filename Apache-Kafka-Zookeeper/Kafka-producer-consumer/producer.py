# from kafka import KafkaProducer
# broker_list = ['localhost:9092','localhost:9094','localhost:9095','localhost:9096','localhost:9097','localhost:9098']
# producer = KafkaProducer(bootstrap_servers=broker_list)
# for _ in range(100):
#     producer.send('arjun-topic', b'some_message_bytes')
import threading, time

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

class Producer(threading.Thread):
    def __init__(self, brokers, topic_name):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.broker_list = brokers
        self.topic = topic_name

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=self.broker_list)

        while not self.stop_event.is_set():
            producer.send(self.topic, b"test")
            producer.send(self.topic, b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()