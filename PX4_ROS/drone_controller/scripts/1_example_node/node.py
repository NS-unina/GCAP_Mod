#!/usr/bin/env python3    

import rospy    


if __name__ == '__main__':  
    # inizializza un nodo ROS con il nome "prova_nodo"
    rospy.init_node("prova_nodo")    

    # stampa messaggi di log sulla console ROS utilizzando le funzioni di logging di ROS
    rospy.loginfo("Ciao sono vivo")    
    rospy.logwarn("questo è un warning dovrebbe apparire giallo")    
    rospy.logerr("questo è un errore deve apparire rosso")

    rospy.sleep(1.0)    # aspetta 1 secondo

    rospy.loginfo("fine programma")    # stampa un messaggio di log sulla console ROS
