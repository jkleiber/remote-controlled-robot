DOCKER_IMG="teleop-img"
DOCKER_CONTAINER="teleop-container"

# Halt duplicate containers
docker stop ${DOCKER_CONTAINER}
docker rm ${DOCKER_CONTAINER}

# Copy the common files to this directory
cp -r ../common ./common

# Run the container
docker run \
    --name ${DOCKER_CONTAINER} \
    -v $(pwd):/teleop \
    -v /dev:/dev \
    --privileged \
    ${DOCKER_IMG}