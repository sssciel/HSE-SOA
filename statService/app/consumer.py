import json
import threading

from kafka import KafkaConsumer
from clickhouse_driver import Client

from statService.app.config import get_clickhouse_url, get_kafka_broker


def start_consumer():
    client = Client.from_url(get_clickhouse_url())
    consumer = KafkaConsumer(
        'likes', 'views', 'comments',
        bootstrap_servers=get_kafka_broker(),
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
    )

    def consume():
        for msg in consumer:
            event = msg.value
            topic = msg.topic
            if topic == 'likes':
                client.execute(
                    'INSERT INTO likes (post_id) VALUES',
                    [{'post_id': event['post_id']}],
                )
            elif topic == 'views':
                client.execute(
                    'INSERT INTO views (post_id) VALUES',
                    [{'post_id': event['post_id']}],
                )
            elif topic == 'comments':
                client.execute(
                    'INSERT INTO comments (post_id) VALUES',
                    [{'post_id': event['post_id']}],
                )

    thread = threading.Thread(target=consume, daemon=True)
    thread.start()
