#!/usr/bin/env python3    

import rospy    # importa la libreria ROS e il modulo rospy
from std_msgs.msg import String    # importa il messaggio standard String di ROS

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)    # crea un Publisher che pubblica messaggi sul topic "chatter"
    rospy.init_node('talker', anonymous=True)    # inizializza un nodo ROS chiamato "talker"
    rate = rospy.Rate(10)    # imposta una frequenza di 10 

    while not rospy.is_shutdown():
         hello_str = "hello world %s" % rospy.get_time()    # crea il messaggio da pubblicare, utilizzando l'istante di tempo corrente
         rospy.loginfo(hello_str)    # stampa il messaggio sulla console ROS
         pub.publish(hello_str)    # pubblica il messaggio sul topic "chatter"
         rate.sleep()    # aspetta per mantenere la frequenza di pubblicazione

if __name__ == '__main__':
       try:
           talker()    # avvia la funzione talker()
       except rospy.ROSInterruptException:
           pass    # gestisce l'eccezione che si verifica quando il nodo viene fermato
