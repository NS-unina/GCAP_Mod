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
    packet = [ord('$'), ord('M'), ord('<'), payload_length,
              command] + data + [checksum]

    return bytes(packet)


def send_msp_packet(packet, sock):
    """Invia un pacchetto MSP tramite socket."""
    sock.send(packet)


def set_rc_channels(channels, sock):
    """Imposta i canali RC tramite MSP."""
    # Comando MSP_SET_RAW_RC (200)
    command = 200
    # I canali RC sono inviati come valori interi a 16 bit
    data = []
    for ch in channels:
        data.extend(struct.pack('<h', ch))

    packet = build_msp_packet(command, data)
    send_msp_packet(packet, sock)


def main():
    print()
    print(" _ _ _ _ _     _ _ _  ")
    print("|  _ _    /   /  _ _ / ")
    print("| |    / /   | /       ")
    print("| |   / /    | |       ")
    print("| |__/ /     | |       ")
    print("| |  \ \      \ \ _ _   ")
    print("|_|   \_\      \_ _ _\  ")
    print()
    print("RC command for mission")
    print()

    parser = argparse.ArgumentParser(
        description='Controllo remoto dei canali RC tramite MSP')
    parser.add_argument(
        "--ip", type=str, help='Indirizzo IP del dispositivo da controllare')
    parser.add_argument("--port", type=int,
                        help='Porta del dispositivo da controllare')

    args = parser.parse_args()

    # Crea una connessione socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.ip, args.port))

        while True:
            # A E T R -> 1 2 4 3
            # Imposta tutti gli stick al minimo per 2 secondi
            set_rc_channels([1000, 1200, 1000, 1500, 2000], sock)
            print("stick in posizione 1 - armato")
            time.sleep(2)

            # Imposta tutti gli stick al massimo per 3 secondi
            set_rc_channels([1000, 1000, 1000, 1000, 1000], sock)
            print("stick in posizione 2 - disarmato")
            time.sleep(3)


if __name__ == "__main__":
    main()
