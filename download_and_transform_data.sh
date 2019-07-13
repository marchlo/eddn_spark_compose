#!/bin/bash

#Define arguments for the shell script
optspec=":d:-:"
while getopts "$optspec" o; do
    case "${o}" in
        d)
            number_of_datasets=${OPTARG}
            ;;
        -) 
            case "${OPTARG}" in
                datasets=*)
                    number_of_datasets=${OPTARG#*=}
                    ;;
            esac;;
    esac
done

#load data from eddn.io
python3 ./python_files/EDDNClient.py --number_of_datasets=$number_of_datasets
#transform json in csv file as cassandra load preparation 
python3 ./python_files/transform_to_csv.py