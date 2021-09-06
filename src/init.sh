#!/bin/bash

echo "----------------------------------------"
echo "CREATING DOCKER VOLUME AND NETWORK"
echo "----------------------------------------"
docker volume create pgstorage
docker network create heatmap_net
echo "----------------------------------------"
echo "FINISHED, IGNORE ERRORS ABOVE (IF ANY)"
echo "----------------------------------------"
echo "INPUT TABLE NAME TO CREATE:"
read TABLE_NAME
echo "----------------------------------------"
echo "HEATMAP DIMENSIONS"
echo "INPUT WIDTH:"
read TABLE_WIDTH
echo "INPUT HEIGHT:"
read TABLE_HEIGHT
echo "POSTGRES_TABLE=$TABLE_NAME" > ../docker/.env
echo "HEATMAP_WIDTH=$TABLE_WIDTH" >> ../docker/.env
echo "HEATMAP_HEIGHT=$TABLE_HEIGHT" >> ../docker/.env
docker-compose -f ../docker/docker-compose.yml up --build -d
echo "FINISHED TABLE CONFIGURATION"
./cmd/create_table.sh $TABLE_WIDTH $TABLE_HEIGHT
echo "----------------------------------------"
docker-compose -f ../docker/docker-compose.yml logs -f

