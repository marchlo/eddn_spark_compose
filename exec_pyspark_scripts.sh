#!/bin/bash

printf "+----------------------------------------------------------------+\n"
printf "Execute pyspark script\n"
printf "+----------------------------------------------------------------+\n"

docker cp ./compose_cluster/pyspark/eddb_data.py sparkmaster:/../tmp/eddb_data.py
docker exec sparkmaster bash ./spark/bin/spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.11:2.3.2 ../tmp/eddb_data.py

printf "+----------------------------------------------------------------+\n"
printf "Done execution pyspark\n"
printf "+----------------------------------------------------------------+\n"

docker cp sparkmaster:/../tmp/check_cass_data.csv ./compose_cluster/export_data/check_cass_data.csv

