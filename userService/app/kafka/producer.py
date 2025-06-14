import json

from app.config import get_kafka_broker
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=get_kafka_broker(),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)
