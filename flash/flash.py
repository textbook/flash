"""The main application."""

from datetime import datetime, date, timedelta
from json import dumps
import logging
from os import getenv

from flash_services import blueprint
from flask import Flask, jsonify, render_template, request
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.wsgi import WSGIContainer

from .parse import parse_config

logger = logging.getLogger(__name__)

flask_app = Flask(__name__)
flask_app.secret_key = getenv('FLASK_SECRET_KEY', 'youwillneverguessit')
flask_app.register_blueprint(blueprint, url_prefix='/flash_services')

CACHE = {}


CONFIG = parse_config()


@flask_app.route('/')
def home():
    """Home page route."""
    return render_template('home.html', config=CONFIG, title='Flash')


@flask_app.route('/scratchpad')
def scratchpad():
    """Dummy page for styling tests."""
    return render_template(
        'demo.html',
        config=dict(
            project_name='Scratchpad',
            style=request.args.get('style', 'default'),
        ),
        title='Style Scratchpad',
    )


@flask_app.route('/_services')
def services():
    """AJAX route for accessing services."""
    service_map = CONFIG['services']
    return jsonify(
        {name: update_service(name, service_map) for name in service_map}
    )


class ServiceWebSocket(WebSocketHandler):
    # pylint: disable=abstract-method

    def open(self):
        logger.info('WebSocket opened')

    def on_message(self, message):
        logger.debug('received message %r', message)
        if message == 'update':
            service_map = CONFIG['services']
            self.write_message(dumps({
                name: update_service(name, service_map) for name in service_map
            }))

    def on_close(self):
        logger.info('WebSocket closed')


app = Application([
    (r'/_services_ws', ServiceWebSocket),
    (r".*", FallbackHandler, dict(fallback=WSGIContainer(flask_app))),
])


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
