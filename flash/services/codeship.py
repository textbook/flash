"""Defines the Codeship CI service integration."""
import logging

import requests

from .auth import UrlParamMixin
from .core import Service

logger = logging.getLogger(__name__)


class Codeship(UrlParamMixin, Service):
    """Show the current build status on Codeship.

    Arguments:
      api_token (:py:class:`str`): A valid token for the Codeship API.
      project_id (:py:class:`int`): The ID of the Codeship project.

    """

    AUTH_PARAM = 'api_key'
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
            return response.json()
        else:
            logger.error('failed to update Codeship project data')
        return {}
