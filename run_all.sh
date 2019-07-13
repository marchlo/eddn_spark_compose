#!/bin/bash

#create a n node cluster with default configurations 
#2 arguments for number of datasets that will downloaded and for number of spark cluster nodes
optspec=":d:n:-:"
while getopts "$optspec" o; do
    case "${o}" in
        d)
            number_of_datasets=${OPTARG}
            ;;
        n)
            number_of_nodes=${OPTARG}
            ;;
        -) 
            case "${OPTARG}" in
                datasets=*)
                    number_of_datasets=${OPTARG#*=}
                    ;;
                nodes=*)
                    number_of_nodes=${OPTARG#*=}
                    ;;
            esac;;
    esac
done

#load data from eddn.io also transform json in csv file as cassandra load preparation 
bash ./download_and_transform_data.sh --datasets=$number_of_datasets

#create docker cluster including cassandra db and spark cluster
bash ./run_docker_compose.sh --nodes=$number_of_nodes
sleep 30
#create keyspace and table also load data into cassandra
bash ./load_data_into_cassandra.sh

#copy pyspark scripts and execute them
bash ./exec_pyspark_scripts.sh

