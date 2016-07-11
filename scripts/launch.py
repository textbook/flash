import logging
from os import getenv
import sys

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)

from flash import app

if __name__ == '__main__':
    server = HTTPServer(WSGIContainer(app))
    server.listen(int(getenv('PORT', 5000)))
    IOLoop.instance().start()
