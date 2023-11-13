

import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    def forward(source, destination):
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.send(data)

    client_to_remote = threading.Thread(target=forward, args=(client_socket, remote_socket))
    remote_to_client = threading.Thread(target=forward, args=(remote_socket, client_socket))

    client_to_remote.start()
    remote_to_client.start()

def proxy_server(listen_host, listen_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_host, listen_port))
    server.listen(5)

    print(f'[*] Proxy in ascolto su {listen_host}:{listen_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accettata connessione da: {addr[0]}:{addr[1]}')

        client_handler = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
        client_handler.start()


if __name__ == '__main__':
    listen_host = '172.22.0.3'  
    listen_port = 8080  
    remote_host = '172.22.0.2'  
    remote_port = 5762

    proxy_server(listen_host, listen_port, remote_host, remote_port)
