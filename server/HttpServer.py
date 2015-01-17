import socket
import markdown
import sys
import os

def parseUrl(url):
    return []

def parseRequest(request):
    lines = request.split('\n')
    req = []
    for ln in lines:
        ln = ln.replace('\r', '').strip()
        req.append(ln.split(':'))
    req[0] = ['PATH', req[0][0]]
    return req

class Response:
    def __init__(self, content):
        self.content = content
        self.headers = 'HTTP/1.0 200 OK \n Content-type: text/html\n'

    def respond(self):
        return self.headers + '\n' + self.content

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8080
        self.log  = None
        self.client_limit = 100
        self.client_black_list = ()
        self.running = False
        self.clients = []
        self.route_path = '/home/jesse/pythoncode/glacier/root/'
        self.debug = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True
        print("Glacier running on %s:%d..." % (self.host,
                                               self.port))
        print("Ctrl-C to Stop Server\n")

        while self.running:
            c_socket = None
            try:
                client = self.sock.accept()
                c_socket = client[0]
                c_address = client[1]
                if c_address not in client:
                    clients.append(client[1])

                # Recieve Request
                req = c_socket.recv(4096)
                request = parseRequest(req)

                # Log Request
                path = request[0][1]
                items = path.split(' ')
                method = items[0]
                path_url = items[1].strip()
                protocol = items[2].strip()

                print("[%s] '%s' %s"% (method, path_url, protocol))

                # List root folder
                file  = ''
                error = None
                files = os.listdir(self.route_path)
                urls = []
                for i in files:
                    urls.append(i.split('.')[0])

                for i in urls:
                    print(path_url)
                    if path_url == '/' + i:
                        file = i
                    elif path_url == '/':
                        file = 'index'
                    else:
                        error = 404

                # Read Markdown File
                html = ''
                if error:
                    if error == 404:
                        html = 'Error 404. Page not Found.'
                else:
                    file = self.root_path + file + '.md'
                    with open(file, 'r') as f:
                        html = markdown.markdown(f.read())

                # Create Response
                response = Response(html)
                c_socket.send(response.respond())
                c_socket.close()
            except Exception as e:
                if self.debug:
                    print(e)
                self.sock.close()
                print("\nGlacier stopped.")
                sys.exit()
        self.sock.close()
