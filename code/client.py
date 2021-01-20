import time
from struct import pack
import socket
import data_functions

# Starts a client, which periodically sends generated data.
def start_client():
    host = "127.0.0.1"        # The server's hostname or IP address
    port = 65432              # The same port as used by the server.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            generated_data = data_functions.generate_data()
            encoded_data = data_functions.pack_and_encode(generated_data)

            time.sleep(1)
            sock.sendall(encoded_data)

start_client()