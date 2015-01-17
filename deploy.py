# deploy.py

from settings import *
from server import HttpServer
from sys import exit

def deploy():
    # Check all settings are present.
    settings = (
        'site_title',
        'site_author',
        'site_description',
        'server_host',
        'server_port',
        'server_log',
        'client_limit',
        'client_black_list',
        'root_path'
    )

    for i in settings:
        if i not in globals():
            print(i + " variable not found in settings.py")
            exit(1)

    # Create New Server Instance
    server = HttpServer.Server()
    server.host = server_host
    server.port = server_port
    server.log  = server_log

    server.client_limit = client_limit
    server.client_black_list = client_black_list
    server.root_path = root_path
    server.debug = debug

    # Start the server
    server.start()

if __name__ == "__main__":
    deploy()
