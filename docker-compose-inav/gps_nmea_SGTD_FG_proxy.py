import socket
import time

def send_nmea_data(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            for line in data:
                client_socket.sendall(f"{line}\r\n".encode())
                time.sleep(0.2)  
        except ConnectionRefusedError:
            print("Connessione rifiutata. Assicurati che il server sia in ascolto sulla porta specificata.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

def read_nmea_data_from_file(filename):
    try:
        with open(filename, 'r') as file:
            nmea_data = file.readlines()
            return [line.strip() for line in nmea_data]
    except FileNotFoundError:
        print(f"Impossibile trovare il file {filename}")
        return []
    except Exception as e:
        print(f"Si è verificato un errore durante la lettura del file: {e}")
        return []

if __name__ == "__main__":
   
    nmea_filename = "gps_nmea.txt"
    nmea_data = read_nmea_data_from_file(nmea_filename)

    if nmea_data:
        send_nmea_data("172.22.0.3", 8080, nmea_data)
