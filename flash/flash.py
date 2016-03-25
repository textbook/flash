"""The main Flask application."""
import json
from os import path

from flask import Flask, jsonify, render_template, request

from flash.services import SERVICES

app = Flask(__name__)


def parse_config():
    """Parse the configuration file and create required services."""
    file_name = path.join(
        path.abspath(path.dirname(__file__)), 'config.json'
    )
    with open(file_name) as config_file:
        data = json.load(config_file)
    for index, config in enumerate(data['services']):
        if config['name'] not in SERVICES:
            raise ValueError('unknown service {!r}'.format(config['name']))
        data['services'][index] = SERVICES[config['name']](**config)
    return data


CONFIG = parse_config()


@app.route('/')
def home():
    """Home page route."""
    return render_template('home.html', config=CONFIG, title='Flash')


@app.route('/_services')
def services():
    """AJAX route for accessing services.

    Arguments:
      name (:py:class:`str`): The name of the service to update.

    Returns:
      The returned data from the service's update method, as JSON.

    """
    name = request.args.get('name', '', type=str)
    if name:
        for service in CONFIG.get('services', []):
            if service.__class__.__name__.lower() == name.lower():
                return jsonify(service.update() or {})
    return jsonify({})
