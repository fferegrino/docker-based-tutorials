import json
import random
import time
from datetime import datetime

from confluent_kafka import Producer

restaurant_ids = [1, 2, 3, 4, 5]
dish_ids = ["AA", "BB", "CC", "DD", "EE"]

update_count = 0
producer = Producer({"bootstrap.servers": "localhost:9092"})


while True:
    update_count += 1
    restaurant_id = random.choice(restaurant_ids)
    dish_id = random.choice(dish_ids)
    update = {
        "update_count": update_count,
        "restaurant_id": restaurant_id,
        "dish_id": dish_id,
        "timestamp": datetime.now().isoformat(),
    }
    producer.produce("restaurant.raw.updates", json.dumps(update))

    if update_count % 10 == 0:
        print(f"Produced {update_count} messages")

    producer.flush()
    time.sleep(1)
