import logging
from os import getenv
import sys

from flash import app

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(getenv('PORT', 5000)), debug=False)
