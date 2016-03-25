import logging
import sys

from flash import app

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)

if __name__ == '__main__':
    app.run()
