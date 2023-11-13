import socket
import struct
import time
import argparse

def build_msp_packet(command, data):
    """Costruisce un pacchetto MSP."""
    payload_length = len(data)
    checksum = 0

    # Calcola checksum
    checksum ^= payload_length
    checksum ^= command
    for byte in data:
        checksum ^= byte

    # Struttura MSP: ['$' 'M' '<' payload_length command data checksum]
    packet = [ord('$'), ord('M'), ord('<'), payload_length, command] + data + [checksum]

    return bytes(packet)

def send_msp_packet(packet, sock):
    """Invia un pacchetto MSP tramite socket."""
    sock.send(packet)

def set_gps_position(sock, lat, lon):
    """Imposta i dati GPS tramite MSP."""
    # Comando MSP_SET_RAW_GPS (201)
    command = 201

    # Dati GPS: fix, numSat, lat, lon, altitudine, velocità
    fix = 1  # GPS fix
    numSat = 10  # Numero di satelliti
    lat = int(lat * 10000000)  # Latitudine convertita in 1E-7 gradi
    lon = int(lon * 10000000)  # Longitudine convertita in 1E-7 gradi
    altitude = 100  # Altitudine in metri
    speed = 0  # Velocità in cm/s

    # Impacchetta i dati GPS
    data = struct.pack('<BBIIhh', fix, numSat, lat ,lon, altitude, speed)
    data = list(data)

    packet = build_msp_packet(command, data)
    send_msp_packet(packet, sock)

def main():
    parser = argparse.ArgumentParser(description="Send GPS coordinates via MSP protocol.")
    parser.add_argument("--ip", type=str, , help="IP address of the server")
    parser.add_argument("--port", type=int,  help="Port number of the server")
    parser.add_argument("--file", type=str, help="File containing coordinates")
    args = parser.parse_args()

    # Crea una connessione socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.ip, args.port))

        # Leggi latitudine e longitudine da un file
        with open(args.file, 'r') as file:
            for line in file:
                lat, lon = map(float, line.strip().split(','))
                
                # Imposta la posizione GPS utilizzando le coordinate dal file
                print(f"Mando coordinate attacco: {lat}, {lon}")
                set_gps_position(sock, lat, lon)
                time.sleep(0.1)

if __name__ == "__main__":
    main()

