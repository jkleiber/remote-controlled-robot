DOCKER_IMG="teleop-img"
DOCKER_CONTAINER="teleop-container"

# Halt duplicate containers.
docker stop ${DOCKER_CONTAINER}
docker rm ${DOCKER_CONTAINER}

# Copy the common files to this directory.
cp -r ../common ./

# Run the VPN.
sudo wg-quick up wg0

# Run the container.
docker run \
    --name ${DOCKER_CONTAINER} \
    -v $(pwd):/teleop \
    -v /dev:/dev \
    -p 5003:5003 \
    --privileged \
    ${DOCKER_IMG}

# Stop the VPN.
sudo wg-quick down wg0
