"""The main Flask application."""
import json
import logging
from datetime import datetime, date, timedelta
from os import getenv, path

from flask import Flask, jsonify, render_template

from flash.services import define_services

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = getenv('FLASK_SECRET_KEY', 'youwillneverguessit')

CACHE = {}


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
        logger.info('loading configuration from file')
        file_name = path.join(
            path.abspath(path.dirname(__file__)), 'config.json'
        )
        with open(file_name) as config_file:
            data = json.load(config_file)
    data['services'] = define_services(data['services'])
    return data


CONFIG = parse_config()


@app.route('/')
def home():
    """Home page route."""
    return render_template('home.html', config=CONFIG, title='Flash')


@app.route('/scratchpad')
def scratchpad():
    """Dummy page for styling tests."""
    return render_template('demo.html', title='Style Scratchpad')


@app.route('/_services')
def services():
    """AJAX route for accessing services."""
    service_map = CONFIG['services']
    return jsonify(
        {name: update_service(name, service_map) for name in service_map}
    )


def update_service(name, service_map):
    """Get an update from the specified service.

    Arguments:
      name (:py:class:`str`): The name of the service.
      service_map (:py:class:`dict`): A mapping of service names to
        :py:class:`flash.service.core.Service` instances.

    Returns:
      :py:class:`dict`: The updated data.

    """
    if name in service_map:
        service = service_map[name]
        data = service.update()
        if not data:
            logger.warning('no data received for service: %s', name)
        else:
            data['service_name'] = service.service_name
            CACHE[name] = dict(data=data, updated=datetime.now())
    else:
        logger.warning('service not found: %s', name)
    if name in CACHE:
        return add_time(CACHE[name])
    return {}


def add_time(data):
    """And a friendly update time to the supplied data.

    Arguments:
      data (:py:class:`dict`): The response data and its update time.

    Returns:
      :py:class:`dict`: The data with a friendly update time.

    """
    payload = data['data']
    updated = data['updated'].date()
    if updated == date.today():
        payload['last_updated'] = data['updated'].strftime('today at %H:%M:%S')
    elif updated >= (date.today() - timedelta(days=1)):
        payload['last_updated'] = 'yesterday'
    elif updated >= (date.today() - timedelta(days=7)):
        payload['last_updated'] = updated.strftime('on %A')
    else:
        payload['last_updated'] = updated.strftime('%Y-%m-%d')
    return payload
