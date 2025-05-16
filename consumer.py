import locale
from kafka import KafkaConsumer
import json
from datetime import datetime

# Create a consumer instance
consumer = KafkaConsumer(
    'binance-stream',
    bootstrap_servers='broker:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Start consuming
for message in consumer:
     print(message.value)