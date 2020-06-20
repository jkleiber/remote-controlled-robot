DOCKER_IMG="teleop-img"
DOCKER_CONTAINER="teleop-container"

# Halt duplicate containers
docker stop ${DOCKER_CONTAINER}
docker rm ${DOCKER_CONTAINER}

# Run the container
docker run \
    -d \
    -v $(pwd):/teleop \
    -v /dev:/dev \
    --privileged \
    ${DOCKER_IMG}