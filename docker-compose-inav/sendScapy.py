from scapy.all import *
import time

src_ip = "172.22.0.3"
dst_ip = "172.22.0.2"
src_port = 41820
dst_port = 5762

interface = "br-a5214788011f"


file_name = "dati2.txt"


delay = 0.01  


with open(file_name, 'r') as file:
    for line in file:
        custom_data = line.strip()  
        tcp_packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port) / Raw(load=custom_data)
        send(tcp_packet, iface=interface)
        time.sleep(delay)  

print("Pacchetti TCP inviati con successo!")

