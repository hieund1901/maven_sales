This doc describes how to set up CDC pipeline

# Setup local pipeline

## Pre-requisites

- Docker and Docker-compose

## docker-compose

Full pipeline can be launched via docker-compose
It will start:

1. MySQL
2. Zookeeper
3. Debezium MySQL connector

## Connecting to a different MySQL instance(Host)

Log in to MySQL using the root account:

```terminal
    docker exec -it mysql-3t mysql -u root -p
```

Grant access in MySQL server for debezium host

Caution about the security risks about WITH GRANT OPTION, refer manual

```
mysql> GRANT ALL PRIVILEGES ON *.* TO 'mysql'@'%' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
mysql> SHOW GRANTS FOR 'mysql'@'%';
```

## Register Connector Debezium

- Register

```terminal
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @register_mysql.json
```

- Check connector

```terminal
curl -X GET http://localhost:8083/connectors
```

- Delete connector

```terminal
curl -X DELETE http://localhost:8083/connectors/warehouse-connector
```

- Restart

```terminal
curl -X POST http://localhost:8083/connectors/warehouse-connector/restart
```
