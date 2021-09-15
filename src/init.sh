#!/bin/bash

echo "----------------------------------------"
echo "CREATING DOCKER VOLUME AND NETWORK"
echo "----------------------------------------"
docker volume create mgstorage
docker network create heatmap_net
echo "----------------------------------------"
echo "FINISHED, IGNORE ERRORS ABOVE (IF ANY)"
echo "----------------------------------------"
echo "INPUT COLLECTION NAME TO CREATE FOR STORING THE DATA:"
read MONGO_COLLECTION
echo "----------------------------------------"
echo "HEATMAP DIMENSIONS"
echo "INPUT WIDTH:"
read TABLE_WIDTH
echo "INPUT HEIGHT:"
read TABLE_HEIGHT
echo "MONGO_COLLECTION=$MONGO_COLLECTION" > ../docker/.env
echo "HEATMAP_WIDTH=$TABLE_WIDTH" >> ../docker/.env
echo "HEATMAP_HEIGHT=$TABLE_HEIGHT" >> ../docker/.env
docker-compose -f ../docker/docker-compose.yml up --build -d
echo "FINISHED TABLE CONFIGURATION"
echo "----------------------------------------"
docker-compose -f ../docker/docker-compose.yml logs -f

