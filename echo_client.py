import socket


class EchoClient:

    def __init__(self):
        self.__default_port = 12345
        self.__host = '127.0.0.1'

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__host, self.__default_port))
            msg = input('Please say Wazzup! ')
            s.sendall(msg.encode())
            data = s.recv(1024)

        print(f'Received from server: {data.decode()}')


if __name__ == "__main__":
    ec = EchoClient()
    ec.connect()
