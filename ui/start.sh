DOCKER_BASE_IMG="ui-server-image"
CONTAINER_NAME="ui-server"

BUILD_TAG="latest"

# Tag the image
DOCKER_IMG="${DOCKER_BASE_IMG}:${BUILD_TAG}"

# Build the image
docker build . -t ${DOCKER_IMG}

# Stop and delete any old containers
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

# Run the image inside the specified container
docker run \
    -v $(pwd):/ui \
    -p 4200:4200 \
    -p 4201:4201 \
    --net=host \
    --name ${CONTAINER_NAME} \
    "${DOCKER_IMG}"
