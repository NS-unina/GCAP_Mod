# Dockerfile for build ROS noetic PX4 and Gezebo11
This guide provides step-by-step instructions for build and run this dockerfile

## Download the repository and navigate to the folder dock_ros_px4_gaze11
```
   git clone https://github.com/NS-unina/GCAP_Mod.git
   cd ~/dock_ros_px4_gaze11
```
## Run build command
```
docker build -t px4-ros-gazebo11 .
```
## Create Network
```
docker network create --driver bridge px4-network

```

## Before running the run command, launch
```
xhost +local:docker

```
## Launch docker run
```
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb  -v /tmp/.X11-unix:/tmp/.X11-unix:ro  -e DISPLAY=$DISPLAY --network px4-network --name  px4-ros px4-ros-gazebo11 bash

```
## Continue to the relevant directories(each dot indicates one of the 2 views in the terminal )
```
1. cd ~/PX4-Autopilot
2. cd ~/PX4-Autopilot
```

## Launching commands (the number corresponds to the number of the terminal window).
```
1. roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
2. make px4_sitl_default gazebo-classic
```

##  NB to compile only the px4 controller you have to run this command of the direcroty ~/PX4-Autopilot
```
make px4_fmu-v5_default

```
function tested, compile is successful figure out if the command is right and how to edit the px4.lunch file and see what it sends to ros and gazebo 