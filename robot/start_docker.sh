# Developer specific script

source docker_config.sh

# Default build directory
BUILD_DIR="${DOCKER_PATH}/robot-dev/"
BUILD_TAG="dev"

# Docker image and tag
DOCKER_IMG="${DOCKER_BASE_IMG}:${BUILD_TAG}"

# Move dependencies into the docker build context
cp Pipfile* $BUILD_DIR/

# Build the image
docker build $BUILD_DIR -t ${DOCKER_IMG}

# Stop and delete any old containers
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

# Run the image inside the specified container
docker run \
    -d \
    -v /dev/ydlidar:/dev/ydlidar \
    -v /dev/ttyUSB0:/dev/ttyUSB0 \
    -v /dev/video0:/dev/video0 \
    -v /dev/video1:/dev/video1 \
    -v $(pwd):/workspace \
    --privileged \
    --net=host \
    --name ${CONTAINER_NAME} \
    "${DOCKER_IMG}"
