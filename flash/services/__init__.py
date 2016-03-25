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
      config (:py:class:`dict`): The service configuration required.

    Returns:
      :py:class:`dict`: Configured services.

    Raises:
      :py:class:`ValueError`: If a non-existent service is requested.

    """
    services = {}
    for name, settings in config.items():
        if name not in SERVICES:
            raise ValueError('unknown service {!r}'.format(name))
        services[name] = SERVICES[name](**settings)
    return services
