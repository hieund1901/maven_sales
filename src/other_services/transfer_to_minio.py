import redis
import json 
from minio import Minio 
from minio.error import S3Error
from dotenv import load_dotenv 
import os 
import io

load_dotenv()

def connect_redis():
    host = os.getenv('REDIS_HOST')
    port = os.getenv('REDIS_PORT')
    db = os.getenv('REDIS_DB')

    try:
        r = redis.Redis(host=host, port=port, db=db)
        if r.ping():
            print('Connected to Redis')
            return r
    except redis.ConnectionError as e:
        print(f'Error connect to Redis: {e}')
        return None
    
def connect_minio():
    end_point = os.getenv('MINIO_ENDPOINT')
    access_key = os.getenv('MINIO_ACCESS_KEY')
    secret_key = os.getenv('MINIO_SECRET_KEY')

    try:
        minio_client = Minio(end_point, access_key=access_key, secret_key=secret_key, secure=False)
        print('Connected to Minio')
        return minio_client
    except Exception as e:
        print(f'Error coonect to Minio: {e}')
        return None 

def transfer_to_minio(minio_client, redis_conn):
    bucket_name = os.getenv('MINIO_BUCKET_NAME')

    try:
        keys = redis_conn.keys('cdc:sales:*')
        for key in keys:
            data = redis_conn.get(key)
            # print(f'Raw data from Redis for key {key.decode("utf-8")}: {data}')

            if data:
                data_dict = json.loads(data.decode('utf-8'))
                json_data = json.dumps(data_dict)
                json_bytes = json_data.encode('utf-8')

                json_stream = io.BytesIO(json_bytes)

                # print(f"Type of json_bytes: {type(json_bytes)}")

                object_name = f"{key.decode('utf-8')}.json"

                minio_client.put_object(
                    bucket_name,
                    object_name,
                    data=json_stream,
                    length=len(json_bytes),
                    content_type='application/json'
                )

                print(f'Successfully uploaded {object_name} to MinIO')

                redis_conn.delete(key)
                print(f'Deleted key {key.decode("utf-8")} from Redis')
    except S3Error as e:
        print(f'Error upploading to MinIO: {e}')
    except Exception as e:
        print(f'Error during data transfer: {e}')

def main():
    redis_conn = connect_redis()
    minio_client = connect_minio()

    if redis_conn and minio_client:
        transfer_to_minio(minio_client, redis_conn)

if __name__ == '__main__':
    main()

