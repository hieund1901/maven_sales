from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import pytz


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 15, 9, 1, tzinfo=pytz.timezone('Asia/Ho_Chi_Minh')),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

with DAG(
    'cdc_to_minio',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    run_cdc_to_redis_task = BashOperator(
        task_id='run_cdc_to_redis',
        bash_command='python3 /opt/airflow/src/kafka_consumer/cdc_to_redis.py'
    )

    run_transfer_to_minio_task = BashOperator(
        task_id='run_transfer_to_minio',
        bash_command='python3 /opt/airflow/src/other_services/transfer_to_minio.py'
    )

    run_cdc_to_redis_task >> run_transfer_to_minio_task