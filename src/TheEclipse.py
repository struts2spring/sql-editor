
import logging.config

from src.view.constants import LOG_SETTINGS
from src.view.EditorSplash import MyApp
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process
from threading import Thread


logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    Thread(target=run).start()
    app = MyApp(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
