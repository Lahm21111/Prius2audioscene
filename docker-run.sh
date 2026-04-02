#!/bin/bash

# Define the image name
IMAGE_NAME="Prius2audioscene:latest"
SCENE_NAME="ros2_output"
CAM_FRONTCENTER_TYPE=image_raw
CAM_SECONDARY_TYPE=image_raw

# Define the path on the host to the folder with bags
HOST_BAG_PATH="/media/mario/LaCie/rosbags_prius"
HOST_NUSCENES_PATH="/media/mario/LaCie/nuscenes_converted/output"

mkdir -p $HOST_NUSCENES_PATH

# Run the Docker container
#docker run --rm -it -v "$HOST_BAG_PATH:/app/bags" -e SCENE_NAME="$SCENE_NAME" -e CAM_FRONTCENTER_TYPE="$CAM_FRONTCENTER_TYPE" -e CAM_SECONDARY_TYPE="$CAM_SECONDARY_TYPE" -v "$HOST_NUSCENES_PATH:/app/output" -v "$(pwd)/config:/app/config" $IMAGE_NAME bash
#!/bin/bash
 
# For running from the command line without vs code

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
 
docker run -it \
    --runtime=nvidia \
	--volume=${SSH_AUTH_SOCK}:/ssh_auth_sock \
    --volume=$XSOCK:$XSOCK:rw \
    --volume=$XAUTH:$XAUTH:rw \
    --volume=$HOME/.ssh:/home/vscode/.ssh \
    --volume="$(pwd)":/workspaces/Prius2audioscene \
    --volume=$HOST_NUSCENES_PATH:/workspaces/Prius2audioscene/output \
    --volume=$HOST_BAG_PATH:/workspaces/Prius2audioscene/rosbag \
    --volume=/etc/localtime:/etc/localtime:ro \
    --env="SSH_AUTH_SOCK"=/ssh_auth_sock \
    --env="XAUTHORITY=${XAUTH}" \
    --env="DISPLAY" \
    --env="SCENE_NAME=$SCENE_NAME" \
    --env="CAM_FRONTCENTER_TYPE=$CAM_FRONTCENTER_TYPE" \
    --env="CAM_SECONDARY_TYPE=$CAM_SECONDARY_TYPE" \
    --privileged \
    --network=host \
    --workdir=/workspaces/Prius2audioscene \
	--user=vscode \
    Prius2audioscene:latest \
    bash
