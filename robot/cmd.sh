#!/bin/bash

ARGS="$@"
if [ -z "$ARGS" ]; then
    ARGS="/bin/bash"
fi

# Command something inside docker
docker exec -it robot-container-ros $ARGS