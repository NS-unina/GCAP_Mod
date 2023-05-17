
# Installation Guide: ROS Noetic + Gazebo 11 + PX4 Autopilot +Mavros +QGroundControl  on Ubuntu 20.04 LTS

This guide provides step-by-step instructions for installing ROS Noetic, Gazebo 11,PX4 Autopilot,Mavros and QGroundControl on Ubuntu 20.04 LTS.

## Prerequisites

- Ubuntu 20.04 LTS
- Internet connection

## Installation Steps

1. Install ROS Noetic:
   - Open a terminal and execute the following commands:
     ```
     sudo apt update
     sudo apt install curl gnupg2 lsb-release
     curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
     sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
     sudo apt update
     sudo apt install ros-noetic-desktop-full
     echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
     source ~/.bashrc
     ```
   - Verify the installation by running `roscore` command in a new terminal. If ROS core starts successfully, ROS Noetic is installed correctly.

2. Install Gazebo 11:
   - Open a terminal and execute the following commands:
   
     ```
     sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable focal main" > /etc/apt/sources.list.d/gazebo-stable.list'
     wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
     sudo apt update
     sudo apt install gazebo11 libgazebo11-dev
     ```

3. Install additional dependencies for PX4 Autopilot:
   - Open a terminal and execute the following commands:
     ```
     sudo apt update
     sudo apt install git zip qtcreator cmake build-essential genromfs ninja-build libssl-dev python3-empy protobuf-compiler libprotobuf-dev libeigen3-dev libxml2-utils libopencv-dev python3-pip
     ```

4. Clone PX4 Autopilot repository:
   - Open a terminal and execute the following commands:
     ```
     mkdir -p ~/src
     cd ~/src
     git clone https://github.com/PX4/PX4-Autopilot.git --recursive
     ```
  - Now reboot your computer.


5. Build PX4 Autopilot with Gazebo:
   - Open a terminal and execute the following commands:
     ```
     cd ~/src
     bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
     make px4_sitl gazebo-classic
     ```
   - This command will download additional dependencies and build PX4 Autopilot with Gazebo simulation.

6. Install QGroundControl :
   - Open a terminal and execute the following command :
     ```
     sudo usermod -a -G dialout $USER
     sudo apt-get remove modemmanager -y
     sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
     sudo apt install libqt5gui5 -y
     sudo apt install libfuse2 -y
     ```
   - Logout and login again to enable the change to user permissions.
    - Download [QGroundControl.AppImage](https://d176tv9ibo4jno.cloudfront.net/latest/QGroundControl.AppImage)
    - Install (and run) using the terminal commands:
    ```
       chmod +x ./QGroundControl.AppImage
       ./QGroundControl.AppImage  (or double click)
     ```
7. Install MAVROS and Dependencies + example to launch:
    ```
       sudo apt install ros-noetic-mavros ros-noetic-mavros-extras
       sudo apt-get update
       sudo apt-get install python3-catkin-tools

     ```
    - Install GeographicLib datasets:
        ```

       sudo apt install geographiclib-tools
       cd ~
        wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
        chmod +x install_geographiclib_datasets.sh
        sudo ./install_geographiclib_datasets.sh
        ```
    - Create a catkin workspace:
       ```
        mkdir -p ~/mav_ws/src
        cd ~/mav_ws/src
        catkin_create_pkg offboard_py rospy mavros_msgs
        ```
    - Create a new Python file called offboard_control.py inside the src directory of the offboard_py package:
        ```
        cd ~/mav_ws/src/offboard_py/src
        touch offboard_control.py
        chmod +x offboard_control.py

       ```
    - Paste the following code into offboard_control.py. This code will publish a setpoint to MAVROS using the mavros_msgs/PositionTarget message.:
       ```
        #!/usr/bin/env python3

        import rospy
        from mavros_msgs.msg import PositionTarget

        def setpoint_publisher():
            rospy.init_node('offboard_control_node')
            setpoint_pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget, queue_size=10)
            rate = rospy.Rate(10)

            # Wait for connection
            while not rospy.is_shutdown() and setpoint_pub.get_num_connections() == 0:
                rospy.loginfo("Waiting for connection...")
                rate.sleep()

            # Set the setpoint
            setpoint = PositionTarget()
            setpoint.coordinate_frame = PositionTarget.FRAME_LOCAL_NED
            setpoint.type_mask = PositionTarget.IGNORE_VX + PositionTarget.IGNORE_VY + \
                                PositionTarget.IGNORE_VZ + PositionTarget.IGNORE_AFX + \
                                PositionTarget.IGNORE_AFY + PositionTarget.IGNORE_AFZ + \
                                PositionTarget.FORCE_SET + PositionTarget.IGNORE_YAW_RATE

            setpoint.velocity.x = 3
            setpoint.velocity.y = 0
            setpoint.velocity.z = 0

            while not rospy.is_shutdown():
                setpoint_pub.publish(setpoint)
                rate.sleep()

        if __name__ == '__main__':
            try:
                setpoint_publisher()
            except rospy.ROSInterruptException:
                pass


        ```
    - Create a new launch file called start_offb.launch inside the offboard_py package:
       ```
        cd ~/mav_ws/src/offboard_py
        touch start_offb.launch
       ```
    - Paste the following code into start_offb.launch. This launch file will start Gazebo with the Iris quadcopter and start MAVROS with offboard control enabled:
        ```
            <launch>
                <!-- Start Gazebo with the Iris quadcopter -->
                <include file="$(find gazebo_ros)/launch/empty_world.launch">
                    <arg name="world_name" value="$(find gazebo_ros)/worlds/iris.world"/>
                </include>

                <!-- Start MAVROS with offboard control enabled -->
                <node name="mavros_node" pkg="mavros" type="mavros_node" output="screen" args="--verbose">
                    <param name="~fcu_url" value="udp://:14540@localhost:14557"/>
                    <param name="~gcs_url" value=""/>
                    <param name="~source_system" value="1"/>
                    <param name="~enable_lockstep" value="false"/>
                    <param name="~target_system_id" value="1"/>
                    <param name="~target_component_id" value="1"/>
                    <param name="~sim_enable_ros_time" value="false"/>
                    <param name="~startup_px4_usb_quirk" value="false"/>
                    <param name="~wait_for_actuator_armed" value="true"/>
                    <param name="~actuator_controls_mavmsg_only" value="false"/>
                    <param name="~odom_frame_id" value="odom"/>
                    <param name="~enable_acc" value="false"/>
                    <param name="~acc_mode" value="std_dev"/>
                    <param name="~enable_gyro" value="false"/>
                    <param name="~gyro_mode" value="std_dev"/>
                    <param name="~enable_mag" value="false"/>
                    <param name="~mag_mode" value="std_dev"/>
                    <param name="~enable_baro" value="false"/>
                    <param name="~baro_mode" value="std_dev"/>
                    <param name="~enable_airspeed" value="false"/>
                    <param name="~airspeed_mode" value="std_dev"/>
                    <param name="~enable_gps" value="false"/>
                    <param name="~gps_mode" value="std_dev"/>
                    <param name="~enable_range" value="false"/>
                    <param name="~range_mode" value="std_dev"/>
                    <param name="~control_mode" value="1"/>
                    <param name="~man/control_send_interval" value="0.05"/>
                </node>
            </launch>

    
      ```
    - Build the offboard_py package:
        ```
        cd ~/mav_ws
        catkin build offboard_py

        ```
    - For proper operation,the following source and PATH must be present in the .bashrc file(use nano .bashrc or code .bashrc if you have visual studio installed):
       ```
        source /opt/ros/noetic/setup.bash
        source ~/mav_ws/devel/setup.bash
        export PATH=$PATH:/opt/ros/noetic/share/ros
        export PATH=$PATH:/opt/ros/noetic/share
        export PATH=$PATH:~/mav_ws/src/offboard_py  

       ```
    - Launch Gazebo and MAVROS with offboard control enabled using start_offb.launch.
        ```
        roslaunch offboard_py start_offb.launch

        ```
      
    


## Support

For any issues or questions, please refer to the following resources:

- [ROS Noetic Documentation](http://wiki.ros.org/noetic)
- [Gazebo Documentation](http://gazebosim.org/)
- [PX4 Autopilot Documentation](https://docs.px4.io/master/en/)



# Guide simple exercises for ROS

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
