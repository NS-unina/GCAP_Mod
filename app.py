import rospy
from mavros_msgs.msg import State
from flask import Flask, jsonify

app = Flask(__name__)

# Initialize ROS node
rospy.init_node('fff')

# Create a publisher for MAVROS state topic
state_pub = rospy.Publisher('/mavros/state', State, queue_size=10)

# Define Flask routes for interacting with MAVROS
@app.route('/')
def get_system_status():
    # Wait for the first message on the MAVROS state topic
    rospy.wait_for_message('/mavros/state', State)
    print('Received first message on MAVROS state topic')

    # Retrieve the current MAVROS state
    state = state_pub.last_msg

    # Example: Retrieve system status from the MAVROS state
    mode = state.mode
    armed = state.armed
    connected = state.connected

    print('Retrieved system status from MAVROS state')

    # Return the system status as JSON response
    response = {
        'mode': mode,
        'armed': armed,
        'connected': connected
    }

    print('Sending JSON response:', response)
    return jsonify(response)

# Add more routes and functionalities as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2002, debug=True)
