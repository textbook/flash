"""Functionality for parsing configuration."""

import json
import logging
from os import getenv, path
import re

from flash_services import define_services

logger = logging.getLogger(__name__)


def parse_config():
    """Parse the configuration and create required services.

    Note:
      Either takes the configuration from the environment (a variable
      named ``FLASH_CONFIG``) or a file at the module root (named
      ``config.json``). Either way, it will attempt to parse it as
      JSON, expecting the following format::

          {
            "name": <Project Name>,
            "services": [
              {
                "name": <Service Name>,
                <Service Settings>
              }
            ]
          }

    """
    env = getenv('FLASH_CONFIG')
    if env:
        logger.info('loading configuration from environment')
        data = json.loads(env)
    else:
        data = _parse_file()
    data['project_name'] = data.get('project_name', 'unnamed')
    data['services'] = define_services(data.get('services', []))
    data['style'] = data.get('style', 'default')
    if data.get('end_time'):
        data['end_time'] = repr(data['end_time'])
    return data


def _parse_file():
    """Parse the config from a file.

    Note:
      Assumes any value that ``"$LOOKS_LIKE_THIS"`` in a service
      definition refers to an environment variable, and attempts to get
      it accordingly.

    """
    file_name = path.join(
        path.abspath(path.dirname(path.dirname(__file__))), 'config.json'
    )
    logger.info('loading configuration from file: %r', file_name)
    try:
        data = _read_file(file_name)
    except FileNotFoundError:
        logger.error('no configuration available, set FLASH_CONFIG or '
                     'provide config.json')
        exit()
    for service in data.get('services', []):
        for key, val in service.items():
            if re.match(r'^\$[A-Z_]+$', val):
                env_val = getenv(val[1:])
                if env_val is None:
                    logger.warning('environment variable %r not found', val[1:])
                service[key] = env_val or val
    return data


def _read_file(file_name):
    """Read the file content and load it as JSON.

    Arguments:
      file_name (:py:class:`str`): The filename.

    Returns:
      :py:class:`dict`: The loaded JSON data.

    Raises:
      :py:class:`FileNotFoundError`: If the file is not found.

    """
    with open(file_name) as config_file:
        data = json.load(config_file)
    return data
