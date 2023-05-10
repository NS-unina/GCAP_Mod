#!/usr/bin/env python3    

import rospy    
from std_msgs.msg import String    # importa il messaggio standard String di ROS

def callback(data):
    # questa funzione viene chiamata ogni volta che arriva un messaggio sul topic "chatter"
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
    # questa funzione inizializza un nodo ROS chiamato "listener" e si mette in ascolto del topic "chatter"
    rospy.init_node('listener', anonymous=True)    # il flag anonymous=True permette di eseguire più istanze del nodo "listener" contemporaneamente

    rospy.Subscriber("chatter", String, callback)    # si iscrive al topic "chatter" e si associa la funzione "callback" che verrà chiamata ogni volta che arriva un messaggio

    rospy.spin()    # questa funzione mantiene attivo il nodo finché non viene fermato

if __name__ == '__main__':
    listener()    # si avvia il nodo "listener"
