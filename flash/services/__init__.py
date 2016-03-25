"""Defines the services that can be shown on the dashboard."""

from .codeship import Codeship
from .tracker import Tracker

SERVICES = dict(
    codeship=Codeship,
    tracker=Tracker,
)
""":py:class:`dict`: The services available to the application."""


def define_services(config):
    """Define the service settings for the current app.

    Arguments:
      config (:py:class:`list`): The service configuration required.

    Returns:
      :py:class:`list`: Configured services.

    Raises:
      :py:class:`ValueError`: If a non-existent service is requested.

    """
    services = []
    for settings in config:
        if settings['name'] not in SERVICES:
            raise ValueError('unknown service {!r}'.format(settings['name']))
        services.append(SERVICES[settings['name']](**settings))
    return services
