import socket
import threading
import datetime


class HttpServer:
    COMMAND = 'GET'
    VERSION = 'HTTP/1.1'
    HOST = 'Host:'

    def __init__(self):
        self.http_conf = {}
        self.mime = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def listen(self):
        while True:
            (conn, addr) = self.sock.accept()
            connection_thread = threading.Thread(
                target=self.parse_request, args=(conn,)
                )
            connection_thread.start()

    def parse_request(self, conn):
        request = conn.recv(1024)
        request = request.decode()
        request = request.rstrip('\r\n')
        request = request.split()
        command, path, version, host, address, *rest = request
        if command == HttpServer.COMMAND and\
                version == HttpServer.VERSION and\
                host == HttpServer.HOST and\
                address == conn.getsockname()[0] + ':' + str(conn.getsockname()[1]):
            self.do_GET(path, conn)
        else:
            conn.sendall(b"405 Method Not Allowed\n")
            print("405 Method Not Allowed")
            conn.close()

    def do_GET(self, path, conn):
        file_extention = path.split('.')[-1]
        requested_file = path.split('/')[-1]
        try:
            f = open(requested_file, "r")
        except FileNotFoundError:
            f = None

        if f and file_extention in self.mime:

            data = f.read()
            response = "HTTP/1.1 200 OK\n Connection: close\n"
            response += "Content-Length {}\n".format(len(data))
            response += "Content-Type: {}\n".format(self.mime[file_extention])
            response += "Date: {}\n\n".format(datetime.datetime.now())
            response += data
            print("200 /{}".format(requested_file))
            conn.sendall(str.encode(response))
            conn.close()
            f.close()
        else:
            response = "HTTP/1.1 404 Not Found\n Connection: close\n"
            response += "Content-Length: 0\n"
            response += "Content-Type: Not Found\n"
            response += "Date: {}\n\n".format(datetime.datetime.now())
            conn.sendall(str.encode(response))
            print("404 Not Found")
            conn.close()

    def start(self):
        with open("http.conf", "r") as conf:
            for line in conf:
                (key, values) = line.split()
                self.http_conf[key] = values
        conf.close()

        with open("mime.types", "r") as mimes:
            for line in mimes:
                (key, values) = line.split()
                self.mime[key] = values
        mimes.close()

        self.sock.bind(
            (self.http_conf['address'], int(self.http_conf['port']))
            )
        self.sock.listen(5)
        listen_thread = threading.Thread(
            name="listen_thread", target=self.listen
            )
        listen_thread.start()


if __name__ == '__main__':
    server = HttpServer()
