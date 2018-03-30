import socket
import threading

import utils


NETWORK_PORT = 8000
HOST = '0.0.0.0'
BUFFER_SIZE = 100


class SocketConnection(object):

    def __init__(self):
        self.threads = []

    def create_socket(self):
        # create a raw socket and bind it to the public interface
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, NETWORK_PORT))

        return server_socket

    def run_server(self, method):
        server_socket = self.create_socket()
        while True:
            #server_socket.listen(backlog) backlog specifies max number of unaccepted connections/requests that maybe queued while waiting for server to accept them
            server_socket.listen(50)
            print('Server is listening')
            #accept connection to this socket and create new socket for each client while releasing the old one to listen to other clients
            (client_socket, client_address) = server_socket.accept()
            print(client_socket)
            #create new client thread to process each incoming message
            newthread = threading.Thread(target = method, args = [client_socket,client_address])
            newthread.start()
            self.threads.append(newthread)
            self.waitForThreads()


    def send_data(self, client_socket, client_address):
        print("Sending message")
        data2 = {'s':{'so':'yummy','no':'shit'}}
        fmt_data = utils.serialize(data2)
        client_socket.send(fmt_data)


    def recv_data(self, client_socket, client_address):
        data = client_socket.recv(BUFFER_SIZE)
        if not data: return
        print("received data:", data)
        #self.send_data(client_socket, client_address)
        return data


    def waitForThreads(self, timeout = 10.00):
		''' Send stop signal to threads and wait for them to end '''
		for thread in self.threads:
			thread.join(timeout)


if __name__ == '__main__':
    sc = SocketConnection()
    sc.run_server(sc.recv_data)
