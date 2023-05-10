# GCAP_Mod

# Guide simple exercises for ROS

-[ROS Tutorials official site](http://wiki.ros.org/ROS/Tutorials)

## Prerequisites

**ROS installed (ROS noetic will be used in this tutorial)** 

## Creation of a ROS package
Open a terminal and access the catkin_ws/src folder. If it does not exist, create it:
```bash
   mkdir -p ~/catkin_ws/src
```
Create the package with the catkin_create_pkg command:

```bash
   cd ~/catkin_ws/src
   catkin_create_pkg drone_controller rospy
```
The catkin_create_pkg command creates the basic structure for the package with the specified name, in our case name_package. Also, by specifying the rospy parameter, we are indicating that our package will use the ROS library for Python, rospy.

After creating the package, go to its folder and paste all the contents found in drone_controller to the link below:

```bash
   git clone https://github.com/NS-unina/GCAP_Mod.git
```

Finally compile the package with the catkin_make command:

```bash
   cd ~/catkin_ws
   catkin_make
```
The catkin_make command will compile our package and make it available within our ROS environment.

## Use of the package
```bash
   roscore
```

Open a second terminal and access the catkin_ws folder:

```bash
   cd ~/catkin_ws
```

Activate the ROS environment with the source command:
```bash
   source devel/setup.bash
```

Start the newly created package node:
```bash
   rosrun nome_package nome_file.py
```



## Made By

- [@Alberto-Urraro](https://github.com/cyberTechA)
