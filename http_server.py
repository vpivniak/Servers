import socket
import threading
import configparser
import time
import mimetypes


class HttpServer:

    def __init__(self):
        self.__host = '127.0.0.1'
        self.__port = 12345
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__listen = True
        self.__connects = []
        self.__index_path = 'index.html'
        self.__img_path = 'Image-Porkeri_001.jpg'
        self.__config = configparser.ConfigParser()

    def start(self):
        self.__socket.bind((self.__host, self.__port))
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
            data = connection.recv(2048)
            if not data:
                break

            print(f'Received from client: {data.decode()}')
            raw_data = data.decode().split(' ')
            method = raw_data[0]
            request_url = raw_data[1]
            http_version = raw_data[2]
            print(f'{method} {request_url} {http_version}')

            if method == 'GET' and request_url == '/index.html':
                with open(self.__index_path, 'r') as f:
                    body = f.read()
                    headers = f'HTTP/1.1 200 OK\n' \
                              f'Connection: close\n' \
                              f'Content-Length: {len(body.encode())}\n' \
                              f'Content-Type: {self.type_reader(self.__index_path)}\n' \
                              f'Date: {time.ctime()}\n\n' \
                              f'{body}'
                    print(headers)
                    connection.sendall(headers.encode())
            elif request_url == '/image.jpg':
                with open(self.__img_path, 'r') as f:
                    body = f.read()
                    headers = f'HTTP/1.1 200 OK\n' \
                              f'Connection: close\n' \
                              f'Content-Length: {len(body.encode())}\n' \
                              f'Content-Type: {self.type_reader(request_url.split("/")[-1])}\n' \
                              f'Date: {time.ctime()}\n\n' \
                              f'{body}'
                    print(headers)
                    connection.sendall(headers)

    def stop(self):
        self.__socket.close()

    def type_reader(self, path):

        unknown = "application/octet- stream" # todo

        mime_type, _ = mimetypes.guess_type(path)
        extension = mimetypes.guess_extension(mime_type)
        ext = extension.split('.')[1]
        self.__config.read("settings.ini")
        return self.__config['MimeType'][ext]


if __name__ == "__main__":

    hs = HttpServer()
    try:
        hs.start()
        hs.listen_connects()
    except KeyboardInterrupt:
        hs.stop()
        pass
