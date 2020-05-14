# DB_MIGRATION

## TO RUN MYSQL SERVER BY DOCKER

```

docker-compose up

```

- if you have MYSQL server already, ignore above step

## USAGE OF MIGRATION SCRIPT

```

python wrapper.py -h  --> give detailed info about arguements

python wrapper.py -d </path/directoryname> -u <user> -H <host> -n <database name> -p <password> -P <port> 

```

### PRE INSTALLATION REQUIRED

- docker & docker-compose if you want to use docker based mysql server
- python 2.7
- pymysql & supported dependencies
- mysql client

- create `versionTable` in mysql
```
CREATE TABLE versionTable (version varchar(10) NOT NULL);
INSERT INTO versionTable VALUES("049");
```