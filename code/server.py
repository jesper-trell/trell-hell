import socket
import data_functions

# To-Do List:
# - Add more accept() statements to accept multiple clients.

# Starts server, which receives and prints incoming sensor data.
def start_server():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        conn, addr = sock.accept()
        print ("Connected by", addr)
        while True:
            data = conn.recv(1024)
            temp, humid = data_functions.package_parser(data)

            # Formats and prints the output.
            print(f"The extracted temperature is {temp}.")
            print(f"The extracted humidity is {humid}.")
            print("")

            if not data: 
                break