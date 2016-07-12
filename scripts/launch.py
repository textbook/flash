import logging
from os import getenv
import sys

from tornado.ioloop import IOLoop

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)

from flash import app

if __name__ == '__main__':
    app.listen(int(getenv('PORT', 5000)))
    IOLoop.instance().start()
