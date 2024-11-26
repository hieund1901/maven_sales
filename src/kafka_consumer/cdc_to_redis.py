import redis
import json
from kafka import KafkaConsumer # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()

def connect_redis():
    host  = os.getenv('REDIS_HOST')
    port = int(os.getenv('REDIS_PORT'))
    db = os.getenv('REDIS_DB')
    try:
        r = redis.Redis(host=host, port=port, db=db)
        if r.ping():
            print('Connected to Redis')
            return r
    except redis.ConnectionError as e:
        print(f'Error connect to Redis: {e}')
        return None
    
def connect_kafka():
    topic = os.getenv('KAFKA_TOPIC')
    servers = os.getenv('KAFKA_SERVERS').split(',')
    group_id = os.getenv('KAFKA_GROUP_ID')

    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers = servers,
            auto_offset_reset = 'earliest',
            enable_auto_commit = False,
            group_id = group_id,
            value_deserializer = lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms = 10000
        )
        print(f'Connected to Kafka topic: {topic}')
        return consumer
    except Exception as e:
        print(f'Error connect to Kafka: {e}')
        return None
    
def store_data_to_redis(redis_conn, consumer):
    try:
        print("Waiting for messages...")
        for message in consumer:
            data = message.value
            opportuinity_id = data['payload']['after']['opportunity_id']
            redis_conn.setex(f'cdc:sales:{opportuinity_id}', 604800, json.dumps(data))
            print(f'Stored data for opportunity_id: {opportuinity_id} to Redis')
            consumer.commit()
    except Exception as e:
        print(f'Error storing data to Redis: {e}')

def main():
    redis_conn = connect_redis()

    if redis_conn:
        kafka_consumer = connect_kafka()
        if kafka_consumer:
            store_data_to_redis(redis_conn, kafka_consumer)

if __name__ == '__main__':
    main()