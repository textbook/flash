"""The main Flask application."""
import json
from os import getenv, path

from flask import Flask, jsonify, render_template, request

from flash.services import define_services

app = Flask(__name__)


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
        data = json.loads(env)
    else:
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


@app.route('/_services')
def services():
    """AJAX route for accessing services."""
    name = request.args.get('name', '', type=str)
    if name:
        for service in CONFIG.get('services', []):
            if service.__class__.__name__.lower() == name.lower():
                return jsonify(service.update() or {})
    return jsonify({})
