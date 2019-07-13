#!/bin/bash

#create a n node cluster with default configurations 
optspec=":n:-:"
while getopts "$optspec" o; do
    case "${o}" in
        n)
            number_of_nodes=${OPTARG}
            ;;
        -) 
            case "${OPTARG}" in
                nodes=*)
                    number_of_nodes=${OPTARG#*=}
                    ;;
            esac;;
    esac
done

printf "+-------------------------------------------------+\n"
printf "Creating %s node cluster \n" "$number_of_nodes"       
printf "+-------------------------------------------------+\n"
cd ./compose_cluster

docker-compose build
docker-compose up -d --scale sparkslave=$number_of_nodes

cd ..
printf "\n"
printf "+----------------------------------------------------+\n"
printf "  %s node cluster  up and running    \n" "$number_of_nodes"
printf "  Check status of nodes running 'docker ps -a'        \n" 
printf "+----------------------------------------------------+\n" 
printf "\n"
