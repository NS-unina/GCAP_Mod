import socket
import struct
import time

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

def set_gps_position(sock):
    """Imposta i dati GPS tramite MSP."""
    # Comando MSP_SET_RAW_GPS (201)
    command = 201

    # Dati GPS: fix, numSat, lat, lon, altitudine, velocità
    fix = 1  # GPS fix
    numSat = 10  # Numero di satelliti
    lat = int(40.8406 * 10000000)  # Latitudine convertita in 1E-7 gradi
    lon = int(14.2963 * 10000000)  # Longitudine convertita in 1E-7 gradi
    altitude = 100  # Altitudine in metri
    speed = 0  # Velocità in cm/s

    # Impacchetta i dati GPS
    data = struct.pack('<BBIIhh', fix, numSat, lat ,lon, altitude, speed)
    #data = [1, 5, 201, 238, 45, 24, 85, 59, 223, 4, 8, 3, 51, 0]

    data = list(data) # converto da binario a lista (controllare...)

    packet = build_msp_packet(command, data)
    send_msp_packet(packet, sock)

# Crea una connessione socket TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 5762))

    # Imposta la posizione GPS su Roma
    while True:
        print("mando")
        set_gps_position(sock)
        time.sleep(0.5)
