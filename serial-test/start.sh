DOCKER_IMG="serial_test_image:latest"
CONTAINER_NAME="serial_test_container"

# Build the image
docker build . -t ${DOCKER_IMG}

# Stop and delete any old containers
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

# Run the image inside the specified container
docker run \
    -v /dev:/dev \
    -v $(pwd):/test \
    --privileged \
    --net=host \
    --name ${CONTAINER_NAME} \
    ${DOCKER_IMG}
