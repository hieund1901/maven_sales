import redis
import json
from kafka import KafkaConsumer # type: ignore

def connect_redis(host='localhost', port=6379, db=0):
    try:
        r = redis.Redis(host=host, port=port, db=db)
        if r.ping():
            print('Connected to Redis')
            return r
    except redis.ConnectionError as e:
        print(f'Error connect to Redis: {e}')
        return None
    
def connect_kafka(topic, servers , group_id = 'cdc-group'):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers = servers,
            auto_offset_reset = 'earliest',
            enable_auto_commit = True,
            group_id = group_id,
            value_deserializer = lambda x: json.loads(x.decode('utf-8'))
        )
        print(f'Connected to Kafka topic: {topic}')
        return consumer
    except Exception as e:
        print(f'Error connect to Kafka: {e}')
        return None
    
def store_data_to_redis(redis_conn, consumer):
    try:
        for message in consumer:
            data = message.value
            opportuinity_id = data['payload']['after']['opportunity_id']
            redis_conn.setex(f'cdc:sales:{opportuinity_id}', 60, json.dumps(data))
            print(f'Stored data for opportunity_id: {opportuinity_id} to Redis')
    except Exception as e:
        print(f'Error storing data to Redis: {e}')

def main():
    redis_conn = connect_redis()

    if redis_conn:
        kafka_consumer = connect_kafka('dbserver1.warehouse.sales_pipeline', 'localhost:39092')
        if kafka_consumer:
            store_data_to_redis(redis_conn, kafka_consumer)

if __name__ == '__main__':
    main()