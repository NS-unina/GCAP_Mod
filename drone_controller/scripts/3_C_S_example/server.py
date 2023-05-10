#!/urs/bin/env python3

from __future__ import print_function

from drone_controller.srv import AddTwoInts, AddTwoIntsResponse  # Importa il messaggio di servizio "AddTwoInts" e la risposta "AddTwoIntsResponse"
import rospy  # Importa il modulo rospy

def handle_add_two_ints(req):  # Definisce la funzione di callback che gestisce la richiesta del servizio
    print("Risultato [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))  # Stampa il messaggio di log sulla console del terminale
    return AddTwoIntsResponse(req.a + req.b)  # Restituisce la risposta del servizio

def add_two_ints_server():  # Definisce la funzione del server
    rospy.init_node('add_two_ints_server')  # Inizializza il nodo del server ROS
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)  # Crea un nuovo servizio chiamato "add_two_ints" con il messaggio di servizio "AddTwoInts" e la funzione di callback "handle_add_two_ints"
    print("Pronto per ricevere i due interi.")  # Stampa il messaggio di log sulla console del terminale
    rospy.spin()  # Attende la chiamata del servizio

if __name__ == "__main__":
    add_two_ints_server()  # Avvia la funzione del server se il file è eseguito come script
