DOCKER_IMG="robot_client_image:latest"
CONTAINER_NAME="rc_udp_container"

# Build the image
docker build . -t ${DOCKER_IMG}

# Stop and delete any old containers
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

# Run the image inside the specified container
docker run \
    -v /dev:/dev \
    -v $(pwd):/app \
    --privileged \
    --name ${CONTAINER_NAME} \
    ${DOCKER_IMG}
