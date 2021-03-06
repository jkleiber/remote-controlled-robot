DOCKER_IMG="robot_client_image:latest"
CONTAINER_NAME="rc_udp_container"

# Build the image
docker build . -t ${DOCKER_IMG}

# Stop and delete any old containers
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

# Copy the common files to this directory.
cp -r ../common ./common

# Run the image inside the specified container
docker run \
    -v /dev:/dev \
    -v $(pwd):/app \
    -p 5001:5001 \
    -p 5002:5002 \
    -p 5003:5003 \
    --privileged \
    --net=host \
    --name ${CONTAINER_NAME} \
    ${DOCKER_IMG}

