## Installation MySQL

- Log in to MySQL using the root account:

```terminal
    docker exec -it mysql-3t mysql -u root -p
```

- If the account does not have permission to view the schema warehouse, grant permission using the command:

```terminal
    GRANT ALL PRIVILEGES ON `warehouse`.* TO 'mysql'@'%';
```

- Run the following command to apply the changes:

```terminal
    FLUSH PRIVILEGES;
```
