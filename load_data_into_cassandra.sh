#!/bin/bash

printf "+----------------------------------------------------------------+\n"
printf "Copy data to cassandra docker \n"
printf "+----------------------------------------------------------------+\n"
docker cp ./python_files/cass_csv_data.csv cassandra:/tmp/cass_csv_data.csv
docker cp ./cassandra_files/copy_data.cql cassandra:/tmp/copy_data.cql
printf "+----------------------------------------------------------------+\n"
printf "Import data in cassandra db \n"
printf "+----------------------------------------------------------------+\n"
docker exec -ti cassandra cqlsh -f ./tmp/copy_data.cql
printf "+----------------------------------------------------------------+\n"
printf "Data was wrote to table eddb_data \n"
printf "+----------------------------------------------------------------+\n"