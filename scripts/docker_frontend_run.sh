#!/bin/sh

set -a
source ./.env.sh
set +a

FULL_CONTAINER_NAME=${CONTAINER_NAME}_frontend

echo Stopping previous container if exists...

docker stop $FULL_CONTAINER_NAME 2>/dev/null &&
    echo Stopped ||
    echo Previous container not found

echo Starting container $FULL_CONTAINER_NAME...

docker run --env-file .env.sh --rm -d --name $FULL_CONTAINER_NAME \
    --network ${NETWORK_NAME} \
    -p ${FRONTEND_PORT}:${FRONTEND_PORT} \
    -t $FULL_CONTAINER_NAME:${CONTAINER_TAG}

docker logs -f $FULL_CONTAINER_NAME