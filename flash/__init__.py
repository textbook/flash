"""A project dashboard that works."""
import logging

import requests
import requests_cache

ONE_MINUTE = 60  # expiry time in seconds

requests_cache.install_cache(expire_after=ONE_MINUTE)

from .flash import app

__author__ = 'Jonathan Sharpe'
__version__ = '0.0.1'

logging.getLogger(__name__).addHandler(logging.NullHandler())
