DOCKER_BASE_IMG="robot-image"
CONTAINER_NAME="robot-container"

# Get the build mode for the image
BUILD_MODE="$1"

# Default build directory
BUILD_DIR="robot-base/"
BUILD_TAG="latest"

# Developer mode
if [ "$BUILD_MODE" = "dev" ]; then
    BUILD_DIR="robot-dev/"
    BUILD_TAG="dev"
fi

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
cp -r ../common ./common

# Run the image inside the specified container
docker run \
    -d \
    -v /dev:/dev \
    -v $(pwd):/robot \
    -p 5000:5000 \
    -p 5001:5001 \
    -p 5002:5002 \
    --privileged \
    --net=host \
    --name ${CONTAINER_NAME} \
    "${DOCKER_IMG}"
