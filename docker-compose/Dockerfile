FROM apache/airflow:2.8.1

WORKDIR /app
# Sao chép file requirements.txt từ thư mục root vào container
COPY requirements.txt .

RUN pip install --upgrade pip

# Cài đặt các gói từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Khởi động Airflow webserver
CMD ["airflow", "webserver"]
