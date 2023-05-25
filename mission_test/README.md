# Mission launch guide(python)
This guide provides step-by-step instructions for launching the test mission + full code documentation
## After installing all the necessary components in the guide, proceed as follows.
## Terminator installation (recommended).
```
sudo apt-get install terminator
```
## Creating the directory that will contain the python script
```
cd ~/src/PX4-Autopilot/
mkdir script_10_05_23
touch mission_test.py
chmod +x *
nano mission_test.py or code . (if you have visual studio code available) copy and paste all the code found on github
```
Upon completion of the previous commands,open the terminal and split the views into 5 ---> right-click muose split(as best you can for the space available)

## Continue to the relevant directories(each dot indicates one of the 5 views in the terminal )
```
1. cd ~/src/PX4-Autopilot
2. cd ~/src/PX4-Autopilot
3. cd ~/Scaricati
4. cd ~/src/PX4-Autopilot/script_10_05_23
5. cd ~/src/PX4-Autopilot/script_10_05_23

```
## Launching commands (the number corresponds to the number of the terminal window).
```
1. roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
2. make px4_sitl_default gazebo-classic
3. ./QGroundControl.AppImage
4. rostopic echo /mavros/state
5. python3 mission_test.py 
```
If everything went correctly you will be able to watch the drone perform its mission on QGroundControl


## Documentation
## Libraries needed for proper operation.
```py
#!/usr/bin/env python3
import rospy
from mavros_msgs.msg import Waypoint, WaypointList
from mavros_msgs.srv import WaypointClear, WaypointPush, WaypointPull, CommandBool, SetMode
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import SetModeRequest
```
## Function clear_waypoints()
```py
def clear_waypoints():
    """
    Delete current waypoints.
    :return: None
    """
    rospy.wait_for_service('/mavros/mission/clear')
    try:
        clear_service = rospy.ServiceProxy('/mavros/mission/clear', WaypointClear)
        clear_service()
    except rospy.ServiceException as e:
        rospy.logerr("Failed to call service: %s" % e)
```
The clear_waypoints() function is used to clear all waypoints currently loaded into the flight control system. It uses a ROS service to call the /mavros/mission/clear service provided by MAVROS. If the service call fails, a rospy.ServiceException is generated and an error message is logged.

## Function push_waypoints()

```py
def push_waypoints(waypoints):
    """
    Pushes the specified waypoints.
    :param waypoints: List of waypoints to push
    :type waypoints: list
    :return: None
    """
    rospy.wait_for_service('/mavros/mission/push')
    try:
        push_service = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
        push_service(start_index=0, waypoints=waypoints)  # Pass start_index explicitly
    except rospy.ServiceException as e:
        rospy.logerr("Failed to call service: %s" % e)
```
The push_waypoints(waypoints) function is used to load a list of waypoints specified in the flight control system. It uses a ROS service to call the /mavros/mission/push service provided by MAVROS. The function accepts a waypoints parameter representing the list of waypoints to be loaded. If the service call fails, a rospy.ServiceException is generated and an error message is logged.

## Function pull_waypoints()
```py
def pull_waypoints():
    """
    Retrieves waypoints from the flight control system.
    :return: list of waypoints
    :rtype: list
    """
    waypoint_list_topic = '/mavros/mission/waypoints'
    waypoints = []

    try:
        waypoint_list = rospy.wait_for_message(waypoint_list_topic, WaypointList, timeout=5)
        waypoints = waypoint_list.waypoints
    except rospy.ROSException as e:
        rospy.logerr("Failed to retrieve waypoints: %s" % str(e))

    return waypoints
```
The pull_waypoints() function retrieves the current list of stored waypoints from the flight control system of the drone. It subscribes to the /mavros/mission/waypoints topic and waits for the WaypointList message to be published with a timeout of 5 seconds. If a message is received within the timeout period, the function extracts the list of waypoints from the message object and returns the list. If no message is received, or an exception occurs, an error message is logged and an empty list is returned.

## Function create_waypoint()
```py
def create_waypoint(x, y, z):
    """
    Creates a new waypoint with the specified coordinates.
    param x: Latitude of waypoint
    :type x: float
    :param y: Longitude of the waypoint
    :type y: float
    :param z: Waypoint altitude
    :type z: float
    :return: Waypoint object
    :rtype: Waypoint
    """
    waypoint = Waypoint()
    waypoint.frame = Waypoint.FRAME_GLOBAL_REL_ALT
    waypoint.command = 16
    waypoint.is_current = False
    waypoint.autocontinue = True
    waypoint.param1 = 0
    waypoint.param2 = 0
    waypoint.param3 = 0
    waypoint.param4 = 0
    waypoint.x_lat = x
    waypoint.y_long = y
    waypoint.z_alt = z
    return waypoint
```
The create_waypoint(x, y, z) function is used to create a new waypoint object with the specified coordinates. The x, y and z parameters represent the latitude, longitude and altitude of the waypoint, respectively. The function returns an object of type Waypoint with properties corresponding to the specified values. The FRAME_GLOBAL_REL_ALT frame, command 16 (WAYPOINT), is_current flag to False, automatic waypoint continuation (autocontinue) to True, and parameters param1, param2, param3, and param4 to 0 are set.

## Function position_callback()
```py
def position_callback(data):
    """
    Callback for current location.
    :param data: Data about the current position
    :type data: NavSatFix
    :return: None
    """
    global current_position
    current_position = data
```
The position_callback(data) function is a callback used to handle data about the current position. It is called whenever new position data is received. The data parameter represents the current position data of type NavSatFix. The function updates the global variable current_position with the new data received.

## Function arm_and_takeoff()
```py
def arm_and_takeoff(altitude):
    """
    Performs vehicle arming and takeoff.
    :param altitude: takeoff height
    :type altitude: float
    :return: None
    """
    rospy.wait_for_service('/mavros/cmd/arming')
    rospy.wait_for_service('/mavros/set_mode')
    try:
        arming_client = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode)

        arming_client(True)

        mode_msg = SetModeRequest()
        mode_msg.custom_mode = "AUTO.TAKEOFF"
        response = mode_client(mode_msg)

        rospy.loginfo("In decollo...")
        rospy.sleep(1)
        takeoff_altitude = altitude
        waypoint_takeoff = create_waypoint(current_position.latitude, current_position.longitude, takeoff_altitude)
        push_waypoints([waypoint_takeoff])
        rospy.sleep(1)
        rospy.loginfo("Il veicolo sta decollando a {} metri.".format(takeoff_altitude))
    except rospy.ServiceException as e:
        rospy.logerr("Impossibile chiamare il servizio: %s" % e)
```
The arm_and_takeoff(altitude) function performs the vehicle arming and takeoff procedures for the drone.
The function first waits for the arming and set_mode services of the drone to become available by calling rospy.wait_for_service(). Then, it creates service proxies for these services using rospy.ServiceProxy.
Next, the function calls the arming service using the arm service proxy by passing True as an argument to arm the drone.
Afterwards, the function sets the drone's mode to AUTO.TAKEOFF by creating a SetModeRequest message with a custom_mode field value of AUTO.TAKEOFF and passing it to the mode_client service proxy.
The function then waits for the drone to reach the takeoff altitude by checking the drone's current position altitude against the specified altitude parameter value. Once the drone has reached this altitude, the function logs a message that the takeoff altitude has been reached.
After reaching the takeoff altitude, the function waits for 10 seconds at the current position before continuing to the next step.
Finally, an exception handler checks for rospy.ServiceException errors and logs them along with an error message.

## Function autostart_mission()

```py
def autostart_mission(current_waypoint):
    """
    Starts the autostart mission.
    current paramwaypoint: Current waypoint
    :type current_waypoint: Waypoint
    :return: None
    """
    clear_waypoints()

    waypoints = []
    waypoints.append(current_waypoint)
    waypoints.append(create_waypoint(current_position.latitude + 0.0005, current_position.longitude + 0.0005, 10.0))
    waypoints.append(create_waypoint(current_position.latitude + 0.0005, current_position.longitude - 0.0005, 15.0))
    waypoints.append(create_waypoint(current_position.latitude, current_position.longitude, 10.0))
    push_waypoints(waypoints)

    rospy.sleep(1)

    rospy.loginfo("Waypoints have been loaded successfully")

    rospy.sleep(1)

    mode_msg = SetModeRequest()
    mode_msg.custom_mode = "AUTO.MISSION"
    mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    response = mode_client(mode_msg)

    if response.mode_sent:
        rospy.loginfo("Mode set to AUTO.MISSION. Starting the mission...")
        rospy.sleep(2)  # Pause for 2 seconds to avoid takeoff errors

        
        mission_completed = False
        waypoint_list = pull_waypoints()
        total_waypoints = len(waypoint_list)
        reached_waypoints = 0

        while not rospy.is_shutdown() and not mission_completed:
            waypoint_list = pull_waypoints()  # Retrieve the latest waypoint list

            if reached_waypoints < total_waypoints:
                current_waypoint = waypoint_list[reached_waypoints]

                # Check if the current waypoint has been reached
                if (
                    abs(current_waypoint.x_lat - current_position.latitude) < 0.00005
                    and abs(current_waypoint.y_long - current_position.longitude) < 0.00005
                ):
                    reached_waypoints += 1

            if reached_waypoints >= total_waypoints and total_waypoints > 0:
                mission_completed = True

            if not mission_completed:
                rospy.loginfo("Waiting for mission completion...")

            rospy.sleep(1)

        rospy.loginfo("Mission completed")

        # Land at home
        land_at_home()
    else:
        rospy.logerr("Cannot set the mode to AUTO.MISSION.")
```
The function autostart_mission(current_waypoint) is used to start the autostart mission. It takes the current waypoint current_waypoint as parameter. Within the function, the following operations are performed:

1. The clear_waypoints() function is called to clear the current waypoints.
2. A list of waypoints called waypoints is created. Initially, the current waypoint passed as a parameter is added. Then, three more waypoints are created using the current coordinates and slightly modified latitude, longitude and altitude values. These waypoints represent a simple flight mission.
3. The push_waypoints() function is called by passing the created list of waypoints.
4. A SetModeRequest object is created and set the custom mode to "AUTO.MISSION." Next, the flight mode setting service is called by passing the created message.
5. Check whether the drone has reached each of the waypoints. The function retrieves the latest waypoint list, and if the drone has reached a waypoint, the function increases the reached_waypoints counter and moves on to the next waypoint. If all waypoints have been reached, the mission is considered complete, and the drone moves on to the next step. If the waypoints have not been reached, the function waits another second and checks again until the mission is complete.
6. Log a message indicating that the mission is complete.
7. Call the land_at_home() function to land the drone at its starting position.

## Function land_at_home()
```py
def land_at_home():
    """
    Make the landing at the starting position.
    :return: None
    """
    home_waypoint = create_waypoint(current_position.latitude, current_position.longitude, 0.0)
    push_waypoints([home_waypoint])

    mode_msg = SetModeRequest()
    mode_msg.custom_mode = "AUTO.LAND"
    mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    response = mode_client(mode_msg)

    if response.mode_sent:
        rospy.loginfo("Mode set to AUTO.LAND. Landing at the starting position...")
    else:
        rospy.logerr("Cannot set the mode to AUTO.LAND.")
```
The land_at_home() function is used to land at the starting position. It takes no parameters and returns no value. It performs the following operations:

1. A waypoint called home_waypoint is created using the current coordinates, but with an altitude of 0.0 (landing position).
2. The push_waypoints() function is called by passing the created landing waypoint. This is used to set the landing waypoint as the only waypoint in the mission.
3. A SetModeRequest object is created and set the custom mode to "AUTO.LAND". Next, the flight mode setting service is called by passing the created message.
4. A log message is displayed indicating that the mode has been set to "AUTO.LAND" and that landing at the starting position is about to begin.

## Function main()
```py
def main():
    rospy.init_node('mission_test', anonymous=True)
    # Subscribe to current position
    State()
    rospy.Subscriber('/mavros/state', State, position_callback)

    rospy.Subscriber('/mavros/global_position/global', NavSatFix, position_callback)
    rospy.wait_for_message('/mavros/global_position/global', NavSatFix, timeout=5)

    if current_position is None:
        rospy.logerr("No current position received.")
        return

    arm_and_takeoff(30)

    current_waypoint = create_waypoint(current_position.latitude, current_position.longitude, 10.0)

    autostart_mission(current_waypoint)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

```
The main() function is the main function of the program. It takes no parameters and returns no values. It performs the following operations:

1. Initializes the ROS node with the name 'mission_test' and anonymous set to True.
2. Subscribes to the /mavros/state and /mavros/global_position/global topics to retrieve the drone's current state and position, respectively.
3. Waits for 5 seconds for a NavSatFix message to be published on the /mavros/global_position/global topic.
4. Checks that we have a valid current position for the drone.
5. Calls the arm_and_takeoff() function with a takeoff altitude of 30.0 meters.
6. Creates a new waypoint at the current drone's position using create_waypoint() function.
7. Calls the autostart_mission() function with the previously created waypoint as an argument to start the drone's autonomous mission.


## Made by
- [Alberto Urraro](https://github.com/cyberTechA)

