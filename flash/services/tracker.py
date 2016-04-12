"""Defines the Pivotal Tracker service integration."""

from collections import defaultdict
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

    def __init__(self, *, api_token, project_id, **kwargs):
        super().__init__(api_token=api_token, **kwargs)
        self.project_id = project_id
        self.project_version = 0
        self._cached = dict(name='unknown', velocity='unknown')

    def details(self, iteration):
        """Update the project data with more details.

        Arguments:
          iteration (:py:class:`int`): The current iteration number.

        Returns:
          :py:class:`dict`: Additional detail on the current iteration.

        """
        url = self.url_builder(
            '/projects/{id}/iterations/{number}',
            {'number': iteration, 'id': self.project_id},
            {'fields': ':default,velocity,stories'},
        )
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            update = response.json()
            return dict(
                stories=self.story_summary(update.get('stories', [])),
                velocity=update.get('velocity', 'unknown'),
            )
        else:
            logger.error('failed to update project iteration details')
        return {}

    @staticmethod
    def story_summary(stories):
        """Get a summary of stories in each state.

        Arguments:
          stories (:py:class:`list`): A list of stories.

        Returns:
          :py:class:`collections.defaultdict`: Summary of points by
            story state.

        """
        result = defaultdict(int)
        for story in stories:
            result[story['current_state']] += int(story.get('estimate', 0))
        return result

    def update(self):
        url = self.url_builder('/projects/{id}', {'id': self.project_id})
        logger.debug('fetching Tracker project data')
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            new_version = int(response.headers.get(
                'X-Tracker-Project-Version', 0,
            ))
            if new_version > self.project_version:
                raw_data = response.json()
                data = {key: raw_data.get(key) for key in ['name', ]}
                logger.debug('project updated, fetching iteration details')
                data.update(self.details(raw_data['current_iteration_number']))
                self.project_version = new_version
                self._cached = data
                return data
            return self._cached
        logger.error('failed to update Tracker project data')
        return {}
