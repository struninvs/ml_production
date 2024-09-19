#!/bin/sh

set -a
source ./.env.sh
set +a
FULL_CONTAINER_NAME=${CONTAINER_NAME}_backend

docker build -f ./backend/Dockerfile --build-arg BACKEND_PORT=${BACKEND_PORT} -t $FULL_CONTAINER_NAME:${CONTAINER_TAG} ./backend