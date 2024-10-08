#1/bin/bash

COMPOSE_FILES="-f airflow.yml -f database.yml -f kafka_cluster.yml -f redis_cluster.yml -f superset.yml -f minio_local_storage.yml"

echo "Starting Docker Compose with the following files: $COMPOSE_FILES"

docker-compose $COMPOSE_FILES up -d

# echo "Checking container status..."
# docker-compose ps

# Lệnh để dừng Docker Compose (nếu cần chạy riêng)
# docker-compose $COMPOSE_FILES down

# Lệnh để thực thi: ./run.sh
