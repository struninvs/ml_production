#!/bin/sh

set -a
source ./.env.sh
set +a
FULL_CONTAINER_NAME=${CONTAINER_NAME}_frontend

docker build -f ./frontend/Dockerfile --build-arg FRONTEND_PORT=${FRONTEND_PORT} -t $FULL_CONTAINER_NAME:${CONTAINER_TAG} ./frontend