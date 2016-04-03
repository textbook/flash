"""A project dashboard that works."""
import logging

from .flash import app

__author__ = 'Jonathan Sharpe'
__version__ = '0.0.1'

logging.getLogger(__name__).addHandler(logging.NullHandler())
