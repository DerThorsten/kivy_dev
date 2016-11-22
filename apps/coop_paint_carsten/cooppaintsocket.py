import socket
import struct

class CoopPaintSocket(socket.socket):
    """
    A socket that can send/receive specialized messages for our coop-paint setup
    """
    MAX_WAITING_CONNECTIONS = 10
    RECV_BUFFER = 4096
    RECV_MSG_LEN = 4

    def __init__(self, host, port):
        """
        Sets up the socket and immediately connects it to the given address and port, or starts listening
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))

    def _send(self, sock, msg):
        """
        Prefixes each message with a 4-byte length before sending.
 
        :param sock: the incoming socket
        :param msg: the message to send
        """
        # Packs the message with 4 leading bytes representing the message length
        msg = struct.pack('>I', len(msg)) + msg
        # Sends the packed message
        sock.sendall(msg)
 
    def _receive(self, sock):
        """
        Receives an incoming message from the client and unpacks it.
 
        :param sock: the incoming socket
        :return: the unpacked message
        """
        data = None
        # Retrieves the first 4 bytes from the message
        tot_len = 0
        while tot_len < self.RECV_MSG_LEN:
            msg_len = sock.recv(self.RECV_MSG_LEN)
            if not msg_len:
                return None
            tot_len += len(msg_len)
        # If the message has the 4 bytes representing the length...
        if msg_len:
            data = ''
            # Unpacks the message and gets the message length
            msg_len = struct.unpack('>I', msg_len)[0]
            tot_data_len = 0
            while tot_data_len < msg_len:
                # Retrieves the chunk i-th chunk of RECV_BUFFER size
                chunk = sock.recv(self.RECV_BUFFER)
                # If there isn't the expected chunk...
                if not chunk:
                    data = None
                    break # ... Simply breaks the loop
                else:
                    # Merges the chunks content
                    data += chunk
                    tot_data_len += len(chunk)
        return data

    def send(self, msg):
        """
        Prefixes each message with a 4-byte length before sending.
        Blocks until sent
 
        :param msg: the message to send
        """
        self._send(self.socket, msg)
 
    def receive(self):
        """
        Receives an incoming message from the client and unpacks it, 
        and blocks until a full message is received.
 
        :return: the unpacked message
        """
        return self._receive(self.socket)

    def close(self):
        self.socket.close()
