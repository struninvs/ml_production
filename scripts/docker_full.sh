#!/bin/sh

set -a
source ./.env.sh
set +a

FULL_CONTAINER_NAME_FRONTEND=${CONTAINER_NAME}_frontend
FULL_CONTAINER_NAME_BACKEND=${CONTAINER_NAME}_backend

echo Building backend image...

docker build -f ./backend/Dockerfile --build-arg BACKEND_PORT=${BACKEND_PORT} -t $FULL_CONTAINER_NAME_BACKEND:${CONTAINER_TAG} ./backend

echo Building frontend image...

docker build -f ./frontend/Dockerfile --build-arg FRONTEND_PORT=${FRONTEND_PORT} -t $FULL_CONTAINER_NAME_FRONTEND:${CONTAINER_TAG} ./frontend

echo Stopping previous backend container if exists...

docker stop $FULL_CONTAINER_NAME_BACKEND 2>/dev/null &&
    echo Stopped ||
    echo Previous container not found

echo Stopping previous frontend container if exists...

docker stop $FULL_CONTAINER_NAME_FRONTEND 2>/dev/null &&
    echo Stopped ||
    echo Previous container not found

echo "Stopping and removing network if it exists..."

docker network rm ${NETWORK_NAME} 2>/dev/null &&
    echo "Network ${NETWORK_NAME} removed." ||
    echo "Network ${NETWORK_NAME} not found."

echo Creating network ${NETWORK_NAME}...

docker network create ${NETWORK_NAME}

echo Starting backend container $FULL_CONTAINER_NAME_BACKEND...

docker run --env-file .env.sh --rm -d --name $FULL_CONTAINER_NAME_BACKEND \
    --network ${NETWORK_NAME} \
    -p ${BACKEND_PORT}:${BACKEND_PORT} \
    -t $FULL_CONTAINER_NAME_BACKEND:${CONTAINER_TAG}

echo Starting frontend container $FULL_CONTAINER_NAME_FRONTEND...

docker run --env-file .env.sh --rm -d --name $FULL_CONTAINER_NAME_FRONTEND \
    --network ${NETWORK_NAME} \
    -p ${FRONTEND_PORT}:${FRONTEND_PORT} \
    -t $FULL_CONTAINER_NAME_FRONTEND:${CONTAINER_TAG}