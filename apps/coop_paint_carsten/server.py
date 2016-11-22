import cooppaintsocket
import threading
import socket
import select
import time

class CoopPaintServer(cooppaintsocket.CoopPaintSocket, threading.Thread):
    def __init__(self, host, port):
        """
        Sets up the server and starts listening
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = None
        self.connections = []  # collects all the incoming connections
        self.running = True  # tells whether the server should run

    def _bind(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.MAX_WAITING_CONNECTIONS)
        self.connections.append(self.socket)
        print("Server listening at {}:{}".format(self.socket.getsockname(), self.port))

    def _broadcast(self, client_socket, client_message):
        """
        Broadcasts a message to all the clients different from both the server itself and
        the client sending the message.
 
        :param client_socket: the socket of the client sending the message
        :param client_message: the message to broadcast
        """
        for sock in self.connections:
            is_not_the_server = sock != self.socket
            is_not_the_client_sending = sock != client_socket
            if is_not_the_server and is_not_the_client_sending:
                try:
                    self._send(sock, client_message)
                except socket.error:
                    # Handles a possible disconnection of the client "sock" by...
                    sock.close()  # closing the socket connection
                    self.connections.remove(sock)  # removing the socket from the active connections list

    def _run(self):
        """
        Actually runs the server.
        """
        while self.running:
            # Gets the list of sockets which are ready to be read through select non-blocking calls
            # The select has a timeout of 60 seconds
            try:
                print("Selecting")
                ready_to_read, ready_to_write, in_error = select.select(self.connections, [], [], 60)
                print("did select, got {} ready to reads".format(len(ready_to_read)))
            except socket.error:
                print("Socket error 1")
                continue
            else:
                for sock in ready_to_read:
                    # If the socket instance is the server socket...
                    if sock == self.socket:
                        try:
                            # Handles a new client connection
                            client_socket, client_address = self.socket.accept()
                        except socket.error:
                            print("Socket error 2")
                            break
                        else:
                            self.connections.append(client_socket)
                            print "Client (%s, %s) connected" % client_address
                    # ...else is an incoming client socket connection
                    else:
                        try:
                            print("Receiving message...")
                            clientName = sock.getsockname()
                            data = self._receive(sock) # Gets the client message...
                            print("Got message from {}".format(clientName))
                            if data:
                                # ... and broadcasts it to all the connected clients
                                print("broadcasting data that was coming from {}".format(clientName))
                                self._broadcast(sock, data)
                            else:
                                print("Client {} closed the connection".format(clientName))
                                sock.close()
                                self.connections.remove(sock)    
                        except socket.error:
                            print "Client %s is offline" % sock.getsockname()
                            sock.close()
                            self.connections.remove(sock)
                            continue
        # Clears the socket connection
        self.stop()

    def send(self, msg):
        self._broadcast(self.socket, msg)

    def receive(self):
        raise NotImplementedError("Server may not receive")

    def close(self):
        # close only allowed by shutting down the server
        self.stop()
 
    def run(self):
        """ Run the server """
        self._bind()
        self._run()

    def stop(self):
        """
        Stops the server by setting the "running" flag before closing
        the socket connection.
        """
        self.running = False
        self.socket.close()

def main():
    try:
        coopPaintServer = CoopPaintServer('localhost', 5559)
        coopPaintServer.start()
        print("Server running. Press ctrl+c to quit")

        while True:
            time.sleep(5)

    except:
        print "bringing down server"
        coopPaintServer.stop()    

if __name__ == "__main__":
    main()