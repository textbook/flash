"""Defines the Codeship CI service integration."""
import logging

import requests

from flash.services.core import Service

logger = logging.getLogger(__name__)


class Codeship(Service):

    REQUIRED = {'api_token', 'project_id'}
    ROOT = 'https://codeship.com/api/v1'
    TEMPLATE = 'codeship'

    def __init__(self, *, api_token, project_id, **_):
        super().__init__()
        self.api_token = api_token
        self.project_id = project_id

    def _url_builder(self, endpoint, params=None, url_params=None):
        if url_params is None:
            url_params = {}
        url_params['api_key'] = self.api_token
        return super()._url_builder(endpoint, params, url_params)

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
