FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Rome

# Installazione ROS Noetic
RUN apt-get update && \
    apt-get install -y curl gnupg2 lsb-release wget git  python3-pip && \
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
    sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
    apt-get update && \
    apt-get install -y ros-noetic-desktop-full && \
    echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
    echo "export PATH=\$PATH:/opt/ros/noetic/share/ros" >> ~/.bashrc && \
    echo "export PATH=\$PATH:/opt/ros/noetic/share" >> ~/.bashrc 


# Installazione Gazebo11
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable focal main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
    wget https://packages.osrfoundation.org/gazebo.key -O - | apt-key add - && \
    apt-get update && \
    apt-get install -y gazebo11 libgazebo11-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev && \
    echo "export GSTREAMER_APP_LIBRARIES=/usr/lib/x86_64-linux-gnu/" >> ~/.bashrc && \
    echo "export GSTREAMER_LIBRARIES=/usr/lib/x86_64-linux-gnu/" >> ~/.bashrc

RUN pip install kconfiglib jsonschema jinja2 future


RUN apt-get update && apt-get install -y libgl1-mesa-glx
#RUN apt-get update && apt-get install -y \
    #libxcb-xinerama0 \
 #   libxkbcommon-x11-0
#ENV QT_QPA_PLATFORM xcb

# Dipendenze per PX4 Autopilot
RUN apt-get update && \
    apt-get install -y git zip qtcreator cmake build-essential pkg-config gcc g++  genromfs ninja-build libssl-dev python3-empy protobuf-compiler libprotobuf-dev libeigen3-dev libxml2-utils libopencv-dev python3-pip

#mavros

RUN apt-get update && \
    apt-get install -y \
    ros-noetic-mavros \
    ros-noetic-mavros-extras \
    geographiclib-tools \
    && wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh \
    && chmod +x install_geographiclib_datasets.sh \
    && ./install_geographiclib_datasets.sh


# add cpio
RUN apt-get install cpio libncurses5 -y

# get the toolchain
RUN wget https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2 -O gcc-arm-none-eabi.tar.bz2

# unpack the archive to a neatly named target directory
RUN mkdir gcc-arm-none-eabi && tar xjfv gcc-arm-none-eabi.tar.bz2 -C gcc-arm-none-eabi --strip-components 1
# remove the archive
RUN rm gcc-arm-none-eabi.tar.bz2

# add the tools to the path
ENV PATH="/gcc-arm-none-eabi/bin:${PATH}"


# Clone PX4 Autopilot repository
RUN git clone https://github.com/PX4/PX4-Autopilot.git --recursive


