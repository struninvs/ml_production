#!/bin/sh

set -a
source ./.env.sh
set +a

FULL_CONTAINER_NAME_FRONTEND=${CONTAINER_NAME}_frontend
FULL_CONTAINER_NAME_BACKEND=${CONTAINER_NAME}_backend

echo Stopping backend container if exists...

docker stop $FULL_CONTAINER_NAME_BACKEND 2>/dev/null &&
    echo Stopped ||
    echo Previous container not found

echo Deleting backend image if exists...

docker image rm $FULL_CONTAINER_NAME_BACKEND:${CONTAINER_TAG} 2>/dev/null &&
    echo Deleted ||
    echo Previous backend image not found

echo Stopping frontend container if exists...

docker stop $FULL_CONTAINER_NAME_FRONTEND 2>/dev/null &&
    echo Stopped ||
    echo Previous frontend container not found

echo Deleting frontend image if exists...

docker image rm $FULL_CONTAINER_NAME_FRONTEND:${CONTAINER_TAG} 2>/dev/null &&
    echo Deleted ||
    echo Previous frontend image not found

echo "Stopping and removing network if it exists..."

docker network rm ${NETWORK_NAME} 2>/dev/null &&
    echo "Network ${NETWORK_NAME} removed." ||
    echo "Network ${NETWORK_NAME} not found."