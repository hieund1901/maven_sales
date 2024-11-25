from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from cdc_to_redis import connect_kafka
from datetime import datetime, timedelta
import mysql.connector

load_dotenv()

def connect_db():
    db_username = os.getenv('DATABASE_USERNAME')
    db_password = os.getenv('DATABASE_PASSWORD')
    db_name = os.getenv('DATABASE_NAME')
    db_host = os.getenv('DATABASE_HOST')
    db_port = os.getenv('DATABASE_PORT')
    try:
        engine = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_username,
            password=db_password,
            database=db_name
        )
        if engine.is_connected():
            print('Connected to database')
            return engine
        else:
            raise Exception("Failed to connect to the database.")
    except Exception as e:
        print(f'Error connecting to database: {e}')
        return None

def convert_date(days_since_epoch):
    if days_since_epoch is not None:
        return datetime(1970, 1, 1) + timedelta(days=days_since_epoch)
    return None

def store_data_to_db(mysql_conn, consumer):
    try:
        print("Starting to consume messages...")
        for message in consumer:
            # print(f"Received message: {message.value}") 
            if not message.value:
                print("Received empty message.")
                continue

            data = message.value
            operation_type = data['payload']['op']
            record = data['payload']['after'] if data['payload']['op'] != 'd' else data['payload']['before']

            opportunity_id = record['opportunity_id']
            conn = mysql_conn 
            if conn is None:
                raise Exception("Connection is None. Could not establish a connection to the database.")
            
            cursor = conn.cursor()
            
            try:
                engage_date = convert_date(record.get('engage_date'))
                close_date = convert_date(record.get('close_date'))
                if operation_type == 'c':
                    stmt = """ INSERT INTO warehouse.staging_sales_pipeline (opportunity_id, sales_agent, product, account, engage_date, close_date, deal_stage, operation_type, received_at)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                    cursor.execute(stmt, (
                        record.get('opportunity_id'),
                        record.get('sales_agent', ''),
                        record.get('product', ''),
                        record.get('account', ''),
                        engage_date,
                        close_date,
                        record.get('deal_stage', ''),
                        'c',
                        datetime.now()
                    ))
                    print(f'Stored data for opportunity_id: {opportunity_id} to database')
                
                elif operation_type == 'u':
                    stmt = """ UPDATE warehouse.staging_sales_pipeline
                                    SET sales_agent = %s,
                                        product = %s,
                                        account = %s,
                                        engage_date = %s,
                                        close_date = %s,
                                        deal_stage = %s,
                                        operation_type = %s,
                                        received_at = %s
                                    WHERE opportunity_id = %s
                                """
                    cursor.execute(stmt, (
                        record.get('sales_agent', ''),
                        record.get('product', ''),
                        record.get('account', ''),
                        engage_date,
                        close_date,
                        record.get('deal_stage', ''),
                        'u',
                        datetime.now(),
                        record.get('opportunity_id')
                    ))
                    print(f'Updated data for opportunity_id: {opportunity_id} to database')

                elif operation_type == 'd':
                    stmt = """ DELETE FROM warehouse.staging_sales_pipeline
                                    WHERE opportunity_id = %s
                                """
                    cursor.execute(stmt, (
                        record['opportunity_id']
                    ))
                    print(f'Deleted data for opportunity_id: {opportunity_id} from database')

                conn.commit()
                print("Committed transaction")
                
            except Exception as e:
                print(f"Error processing message for opportunity_id {opportunity_id}: {e}")
                conn.rollback()
            finally:
                cursor.close()

    except Exception as e:
        print(f'Error storing data to database: {e}')
        
def main():
    mysql_conn = connect_db()

    if mysql_conn:
        kafka_consumer = connect_kafka()
        if kafka_consumer:
            store_data_to_db(mysql_conn, kafka_consumer)

if __name__ == '__main__':
    main()