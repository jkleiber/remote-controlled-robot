#!/bin/bash

ARGS="$@"

if [ -z $ARGS ]; then
    ARGS="/bin/bash"
fi

docker exec -it robot-container-ros $ARGS