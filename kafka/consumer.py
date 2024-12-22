import json
import random
import time
from datetime import datetime

from confluent_kafka import Consumer

restaurant_ids = [1, 2, 3, 4, 5]
dish_ids = ["AA", "BB", "CC", "DD", "EE"]

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "restaurant-consumer",
        "auto.offset.reset": "earliest",
    }
)
consumer.subscribe(["restaurant.raw.updates"])

last_update_count = 0
last_offset = 0

starting_count = -1
starting_offset = -1

try:
    while True:
        message = consumer.poll(timeout=1.0)
        if message is None:
            continue

        data = json.loads(message.value().decode("utf-8"))
        if last_message_timestamp is None:
            last_message_timestamp = data["timestamp"]

        last_update_count = data.get("update_count", 0)
        last_offset = message.offset()

        if starting_offset == -1:
            starting_offset = last_offset
            starting_count = last_update_count
            print(
                f"Starting at offset {starting_offset} with update count {starting_count}"
            )

except KeyboardInterrupt:
    print(f"Finished at offset {last_offset} with update count {last_update_count}")
finally:
    consumer.close()
