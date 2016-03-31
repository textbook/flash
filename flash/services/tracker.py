"""Defines the Pivotal Tracker service integration."""
import logging
import requests

from .auth import HeaderMixin
from .core import Service

logger = logging.getLogger(__name__)


class Tracker(HeaderMixin, Service):
    """Show the current status of a Pivotal Tracker project.

    Arguments:
      api_token (:py:class:`str`): A valid token for the Tracker API.
      project_id (:py:class:`int`): The ID of the Tracker project.

    Attributes:
      project_version (:py:class:`int`): The current project version,
        used to invalidate the cached data as appropriate.

    """

    AUTH_HEADER = 'X-TrackerToken'
    REQUIRED = {'api_token', 'project_id'}
    ROOT = 'https://www.pivotaltracker.com/services/v5'
    TEMPLATE = 'tracker'

    def __init__(self, *, api_token, project_id, **_):
        super().__init__()
        self.api_token = api_token
        self.project_id = project_id
        self.project_version = 0
        self._cached = dict(name='unknown', velocity='unknown')

    def _get_velocity(self, data):
        """Update the project data with the current velocity.

        Arguments:
          :py:class:`dict`: The project data from the API.

        """
        url = self._url_builder(
            '/projects/{id}/iterations/{number}',
            {'number': data['current_iteration_number'], 'id': self.project_id},
            {'fields': ':default,velocity'},
        )
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            velocity = response.json().get('velocity', 'unknown')
            data['velocity'] = velocity
        else:
            logger.error('failed to update project velocity')

    def update(self):
        url = self._url_builder('/projects/{id}', {'id': self.project_id})
        logger.debug('fetching Tracker project data')
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            new_version = int(response.headers.get(
                'X-Tracker-Project-Version', 0,
            ))
            if new_version > self.project_version:
                data = response.json()
                logger.debug('project updated, fetching velocity')
                self._get_velocity(data)
                self.project_version = new_version
                self._cached = data
                return data
            return self._cached
        else:
            logger.error('failed to update Tracker project data')
        return {}
