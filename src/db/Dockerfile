FROM postgres:16.1

## Empty DB
#COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

## DB with parsed data
COPY ./dump-spotistats-202312142323.sql /docker-entrypoint-initdb.d/init.sql
