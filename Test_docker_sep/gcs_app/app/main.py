#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import NavSatFix
from rospy.topics import Publisher 

from flask import Flask
app = Flask(__name__)

@app.route('/')
def gcs():
    return "Hello GCS!"

@app.route('/position')
def position():
    gps = get_gps()
    return f"Latitude: {gps.latitude}, Longitude: {gps.longitude}"

def get_gps():
    msg = rospy.wait_for_message("/vehicle_gps_position", NavSatFix)
    return msg

if __name__ == "__main__":
    rospy.init_node("gcs")
    
    app.run(host="0.0.0.0", port=8080)