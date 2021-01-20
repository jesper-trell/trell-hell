import threading
import data_functions
import client
import server
import multi_server


CLIENTS = 10

# Starts and runs the server.
server_thread = threading.Thread(target=multi_server.start_server, args=())
server_thread.start()

# Starts a specified number of clients.
for i in range(CLIENTS):
    thread = threading.Thread(target=client.start_client, args=())
    thread.start()