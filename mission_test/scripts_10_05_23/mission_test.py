#!/usr/bin/env python3

import rospy
from mavros_msgs.msg import Waypoint, WaypointList
from mavros_msgs.srv import WaypointClear, WaypointPush, WaypointPull, CommandBool, SetMode
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import SetModeRequest
from mavros_msgs.msg import State

home_position = NavSatFix()
current_position = NavSatFix()

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

def position_callback(data):
    """
    Callback for current location.
    :param data: Data about the current position
    :type data: NavSatFix
    :return: None
    """
    global current_position
    current_position = data

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

        rospy.loginfo("Taking off...")
        rospy.sleep(1)
    
        takeoff_position = current_position
        takeoff_position.altitude = altitude


        # Check if the vehicle has reached the takeoff altitude
        reached_takeoff_altitude = False

        while not rospy.is_shutdown() and not reached_takeoff_altitude:
            rospy.loginfo("Waiting to reach takeoff altitude...")
            rospy.sleep(1)

            # Check the current altitude
            if current_position.altitude >= altitude:
                reached_takeoff_altitude = True

        rospy.loginfo("Takeoff altitude reached")


        # Wait at current position
        rospy.loginfo("Waiting at current position...")
        start_time = rospy.get_rostime()

        while not rospy.is_shutdown():
            elapsed_time = rospy.get_rostime() - start_time
            if elapsed_time.to_sec() >= 10.0:  # Wait for 10 seconds at the current position
                break
            else:
                rospy.sleep(1)

        rospy.loginfo("Wait at current position complete")
        rospy.sleep(2)
        
    except rospy.ServiceException as e:
        rospy.logerr("Failed to call service: %s" % e)

    
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

