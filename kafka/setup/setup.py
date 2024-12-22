import time

from confluent_kafka.admin import AdminClient, NewTopic

# Create topics
kafka_admin = AdminClient({"bootstrap.servers": "broker:29092"})

topics = [
    "restaurant.raw.updates",
]

existing_topics = set(kafka_admin.list_topics().topics)

for topic in topics:
    new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)

    if topic in existing_topics:
        print(f"Deleting topic {topic}")
        kafka_admin.delete_topics([topic])
        time.sleep(3)

    kafka_admin.create_topics([new_topic])
    print(f"Topic {topic} created successfully.")
