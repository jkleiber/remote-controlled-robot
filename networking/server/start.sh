DOCKER_IMG="server_image:latest"
CONTAINER_NAME="server_udp_container"

# Build the image
docker build . -t ${DOCKER_IMG}

# Stop and delete any old containers
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

# Run the image inside the specified container
docker run \
    -v /dev:/dev \
    -v $(pwd):/server \
    --privileged \
    --name ${CONTAINER_NAME} \
    ${DOCKER_IMG}
