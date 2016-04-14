"""Core service description."""

from abc import ABCMeta, abstractmethod
from datetime import datetime

from .utils import naturaldelta


class Service(metaclass=ABCMeta):
    """Abstract base class for services."""

    REQUIRED = set()
    """:py:class:`set`: The service's required configuration keys."""

    ROOT = ''
    """:py:class:`str`: The root URL for the service API."""

    TEMPLATE = 'undefined'
    """:py:class:`str`: The name of the template to render."""

    @abstractmethod
    def __init__(self, *_, **kwargs):
        self.service_name = kwargs.get('name')

    @abstractmethod
    def update(self):
        """Get the current state to display on the dashboard."""
        raise NotImplementedError

    @property
    def headers(self):
        """Get the headers for the service requests."""
        return {}

    def url_builder(self, endpoint, params=None, url_params=None):
        """Create a URL for the specified endpoint.

        Arguments:
          endpoint (:py:class:`str`): The API endpoint to access.
          params: (:py:class:`dict`, optional): The values for format
            into the created URL (defaults to ``None``).
          url_params: (:py:class:`dict`, optional): Parameters to add
            to the end of the URL (defaults to ``None``).

        Returns:
          :py:class:`str`: The resulting URL.

        """
        formatted_params = None
        if url_params:
            formatted_params = '&'.join(
                ['{}={}'.format(key, val) for key, val in url_params.items()]
            )
        return ''.join([
            self.ROOT,
            endpoint,
            '?' + formatted_params if formatted_params else ''
        ]).format(**params or {})

    @classmethod
    def from_config(cls, **config):
        """Manipulate the configuration settings."""
        missing = cls.REQUIRED.difference(config)
        if missing:
            raise TypeError('missing required config keys: {!s}'.format(
                ', '.join(missing)
            ))
        instance = cls(**config)
        return instance

    @staticmethod
    def estimate_time(current, previous):
        """Update the current build with an estimated completion time.

        Takes a simple average over the previous builds, using those
        whose outcome is ``'passed'``.

        Arguments:
          current (:py:class:`dict`): The current build data.
          previous (:py:class:`list`): All previous builds.

        """
        if current.get('started_at') is None:
            current['elapsed'] = 'estimate not available'
            return
        usable = [
            build for build in previous if build['outcome'] == 'passed' and
            build['duration'] is not None
        ]
        if not usable:
            current['elapsed'] = 'estimate not available'
            return
        average_duration = int(sum(build['duration'] for build in usable) /
                               float(len(usable)))
        finish = current['started_at'] + average_duration
        remaining = (datetime.fromtimestamp(finish) -
                     datetime.now()).total_seconds()
        current['elapsed'] = '{} left'.format(naturaldelta(remaining))
