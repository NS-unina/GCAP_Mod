#!/usr/bin/env python3

from __future__ import print_function    

import sys    # importa il modulo sys per l'accesso alle variabili del sistema
import rospy    # importa la libreria ROS e il modulo rospy
from drone_controller.srv import *    # importa il messaggio di servizio AddTwoInts

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')    # attende che il servizio "add_two_ints" sia disponibile
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)    # crea un oggetto ServiceProxy per invocare il servizio
        resp1 = add_two_ints(x, y)    # chiama il servizio con gli argomenti x e y
        return resp1.sum    # restituisce la somma restituita dal servizio
    except rospy.ServiceException as e:    # gestisce eventuali eccezioni che si verificano durante la chiamata al servizio
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]    # restituisce un messaggio di utilizzo del programma

if __name__ == "__main__":
    if len(sys.argv) == 3:    # controlla che il programma sia stato chiamato con due argomenti
        x = int(sys.argv[1])    # converte il primo argomento in un intero
        y = int(sys.argv[2])    # converte il secondo argomento in un intero
    else:
        print(usage())    # stampa il messaggio di utilizzo del programma
        sys.exit(1)    # esce dal programma con codice di errore 1

    print("Richiesta %s+%s"%(x, y))    # stampa il messaggio di richiesta
    print("%s + %s = %s"%(x, y, add_two_ints_client(x, y)))    # chiama il servizio e stampa il risultato
