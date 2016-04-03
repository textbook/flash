"""Defines the Codeship CI service integration."""
import logging

from dateutil.parser import parse
import requests

from .auth import UrlParamMixin
from .core import Service
from .utils import elapsed_time, truncate

logger = logging.getLogger(__name__)


class Codeship(UrlParamMixin, Service):
    """Show the current build status on Codeship.

    Arguments:
      api_token (:py:class:`str`): A valid token for the Codeship API.
      project_id (:py:class:`int`): The ID of the Codeship project.

    """

    AUTH_PARAM = 'api_key'
    OUTCOMES = {
        'success': 'passed',
        'error': 'failed',
        '?': 'crashed',
        '??': 'cancelled',
        '???': 'working',
    }
    REQUIRED = {'api_token', 'project_id'}
    ROOT = 'https://codeship.com/api/v1'
    TEMPLATE = 'codeship'

    def __init__(self, *, api_token, project_id, **kwargs):
        super().__init__(api_token=api_token, **kwargs)
        self.project_id = project_id

    def update(self):
        logger.debug('fetching Codeship project data')
        response = requests.get(
            self._url_builder('/projects/{id}.json', {'id': self.project_id})
        )
        if response.status_code == 200:
            return self.format_data(response.json())
        else:
            logger.error('failed to update Codeship project data')
        return {}

    @classmethod
    def format_data(cls, data):
        """Re-format the response data for the front-end.

        Arguments:
          data (:py:class:`dict`): The JSON data from the response.

        Returns:
          :py:class:`dict`: The re-formatted data.

        """
        return dict(
            builds=[
                cls.format_build(build) for build in data.get('builds', [])
            ],
            name=data.get('repository_name'),
        )

    @classmethod
    def format_build(cls, build):
        """Re-format the build data for the front-end.

        Arguments:
          build (:py:class:`dict`): The JSON data from the response.

        Returns:
          :py:class:`dict`: The re-formatted data.

        """
        try:
            elapsed = elapsed_time(
                parse(build.get('started_at')),
                parse(build.get('finished_at')),
            )
        except (AttributeError, ValueError):
            logger.exception('failed to parse time data')
            elapsed = 'Elapsed time not available'
        status = build.get('status')
        if status not in cls.OUTCOMES:
            logger.warning('unknown status: %s', status)
        return dict(
            author=build.get('github_username'),
            elapsed=elapsed,
            message=truncate(build.get('message')),
            outcome=cls.OUTCOMES.get(status),
        )
