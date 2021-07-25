import socket
import threading


class EchoServer:

    def __init__(self, d_port=12345):
        self.__default_port = d_port
        self.__host = '127.0.0.1'
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__listen = True
        self.__connects = []

    def is_running(self):
        return self.__listen

    @property
    def port(self):
        return self.__default_port

    def start(self):
        self.__socket.bind((self.__host, self.__default_port))
        self.__socket.listen(5)

    def listen_connects(self):
        while self.__listen:
            connection, client_address = self.__socket.accept()
            print(f'connection from {client_address}')
            self.__connects.append(connection)
            self.add_connects_to_thread(connection)

    def add_connects_to_thread(self, connection):
        t = threading.Thread(target=self.read, args=(connection,))
        t.start()
        print(f'{t.name}')

    def read(self, connection):
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f'Received from client: {data.decode()}')
            if data == b'stop\r\n':
                connection.close()
                print('disconnect')
                break
            elif data == b'quit\r\n':
                self.__listen = False
                for connect in self.__connects:
                    connect.close()
                self.stop()
                print('socket connection closed')
                break
            if data:
                print('sending data back to the client')
                connection.sendall(data)

    def stop(self):
        self.__socket.close()


if __name__ == "__main__":
    es = EchoServer()
    try:
        # es.is_running()
        es.start()
        es.listen_connects()
        # es.is_running()
        # es.stop()
        # es.is_running()
        # print(es.port)
        # es = EchoServer(54321)
        # print(es.port)
        # es.is_running()
        # es.start()
        # es.is_running()
        # es.stop()
    except KeyboardInterrupt:
        es.stop()
        pass
