import socket
import threading


class EchoServer:
    def __init__(self, port=1521):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.is_running = False
        self.connections = []

    def listen(self):
        while self.is_running:
            (conn, addr) = self.sock.accept()
            self.connections.append(conn)
            connection_thread = threading.Thread(
                    target=self.connection, args=(conn,))
            connection_thread.start()
        conn.close()

    def connection(self, conn):
        while self.is_running:
            chunk = conn.recv(1024)
            if chunk == b"disconnect\r\n" or not chunk:
                conn.close()
                self.connections.remove(conn)
                break
            conn.sendall(chunk)

    def start(self):
        self.is_running = True
        self.sock.bind(('localhost', self.port))
        self.sock.listen(5)

        listen_thread = threading.Thread(
                name="listen_thread", target=self.listen)
        listen_thread.start()

    def stop(self):
        self.is_running = False
        self.sock.close()
        for e in self.connections:
            e.close()


if __name__ == '__main__':
    my_socket = EchoServer(5556)
    my_socket.start()
    print(my_socket.is_running)
    print(my_socket.port)
    temp = input("enter 1 to stop:")
    if temp == '1':
        my_socket.stop()

    print(my_socket.is_running)
    print(my_socket.port)
