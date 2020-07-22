# Developer specific script

DOCKER_BASE_IMG="robot-image-ros"
CONTAINER_NAME="robot-container-ros"

# Default build directory
BUILD_DIR="robot-ros-dev/"
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

# Copy the common files to this directory.
cp -r ../common ./

# Run the image inside the specified container
docker run \
    -d \
    -v /dev:/dev \
    -v $(pwd):/robot \
    --privileged \
    --net=host \
    --name ${CONTAINER_NAME} \
    "${DOCKER_IMG}"

echo "Docker container started!"