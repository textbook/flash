"""Defines the services that can be shown on the dashboard."""

from collections import OrderedDict
from uuid import uuid4

from .codeship import Codeship
from .github import GitHub
from .tracker import Tracker
from .travis import TravisOS

SERVICES = dict(
    codeship=Codeship,
    github=GitHub,
    tracker=Tracker,
    travis=TravisOS,
)
""":py:class:`dict`: The services available to the application."""


def define_services(config):
    """Define the service settings for the current app.

    Arguments:
      config (:py:class:`list`): The service configuration required.

    Returns:
      :py:class:`collections.OrderedDict`: Configured services.

    Raises:
      :py:class:`ValueError`: If a non-existent service is requested.

    """
    services = OrderedDict()
    for settings in config:
        name = settings['name']
        if name not in SERVICES:
            raise ValueError('unknown service {!r}'.format(name))
        services[uuid4().hex] = SERVICES[name].from_config(**settings)
    return services
