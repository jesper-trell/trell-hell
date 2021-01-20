import socket
import selectors
import types
import data_functions

# Starts server with capability of accepting multiple concurrent clients.
def start_server():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


    # Starts host server and selector to allow multiplexing.
    sel = selectors.DefaultSelector()
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    print(f"Listening on ({HOST}, {PORT}).")

    while True:
        # Blocks until there are sockets ready for I/O.
        events = sel.select(timeout=None)

        # Accepts new connections and services already connected ones.
        # Socket object and data is stored in key, while mask stores the events.
        for key, mask in events:
            if key.data is None:
                accept_wrapper(sel, key.fileobj)
            else:
                service_connection(sel, key, mask)


# Accepts a new incoming client.
def accept_wrapper(sel, sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")

    #  To know when client connection is ready reading and writing.
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    print(f"Accepted connection from {addr}.")


# Services an already connected client.
def service_connection(sel, key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}.")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            temp, humid = data_functions.package_parser(data.outb)

            # Formats and prints the output.
            print(f"Received data from {data.addr}:")
            print(f"The extracted temperature is {temp}.")
            print(f"The extracted humidity is {humid}.")
            print("")

            # Sends data to the client.
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:] 