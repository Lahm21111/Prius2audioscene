FROM ros:humble-ros-base

ENV DEBIAN_FRONTEND=noninteractive

ENV ROS_DISTRO=humble

# 更换 apt 源为阿里云（提升国内下载速度）
RUN sed -i 's@http://archive.ubuntu.com@http://mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@http://security.ubuntu.com@http://mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@http://ports.ubuntu.com@http://mirrors.aliyun.com@g' /etc/apt/sources.list 2>/dev/null || true

# Update all packages
RUN sudo apt update \
    && sudo apt install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-opencv \
    git \
    ros-${ROS_DISTRO}-sensor-msgs-py \
    ros-${ROS_DISTRO}-rosbag2-storage-mcap \
    ros-${ROS_DISTRO}-cv-bridge \
    git-core \    
    bash-completion \
    vim \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

# 更换 pip 源为清华源（提升 Python 包下载速度）
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
# # 配置 pip 使用清华源
# RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip3 install -r requirements.txt -v
COPY nuscenes-devkit /nuscenes-devkit
# RUN pip install -e /nuscenes-devkit/setup

################
# Expose the nvidia driver to allow opengl 
# Dependencies for glvnd and X11.
################
RUN sudo apt update \
    && sudo apt install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-opencv \
    git \
    ros-${ROS_DISTRO}-sensor-msgs-py \
    ros-${ROS_DISTRO}-rosbag2-storage-mcap \
    ros-${ROS_DISTRO}-cv-bridge \
    git-core \    
    bash-completion \
    vim \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute
ENV QT_X11_NO_MITSHM=1

# Add vscode user with same UID and GID as your host system
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # Add sudo support for the non-root user
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Add user to video group to allow access to webcam
RUN usermod --append --groups video $USERNAME

# Set up auto-source of workspace for ros user
ARG WORKSPACE=/app

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /home/$USERNAME/.bashrc
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/$USERNAME/.bashrc

# Now we source the bashrc_local in the bashrc 

# Switch from root to user
USER $USERNAME