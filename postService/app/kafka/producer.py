import json

from kafka import KafkaProducer

from postService.app.config import get_kafka_broker

producer = KafkaProducer(
    bootstrap_servers=get_kafka_broker(),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)
