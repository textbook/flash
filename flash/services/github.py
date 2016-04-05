"""Defines the GitHub service integration."""

import logging

import requests

from .auth import UrlParamMixin
from .core import Service
from .utils import occurred, truncate


logger = logging.getLogger(__name__)


class GitHub(UrlParamMixin, Service):
    """Show the current status of a GitHub repository.

    Arguments:
      api_token (:py:class:`str`): A valid token for the GitHub API.
      account (:py:class:`str`): The name of the account.
      app (:py:class:`str`): The name of the application.

    Attributes:
      repo (:py:class:`str`): The repository name, in the format
        ``account/application``.

    """

    AUTH_PARAM = 'access_token'
    REQUIRED = {'api_token', 'account', 'app'}
    ROOT = 'https://api.github.com'
    TEMPLATE = 'github'

    def __init__(self, *, api_token, account, app, **kwargs):
        super().__init__(api_token=api_token, **kwargs)
        self.account = account
        self.app = app
        self.repo = '{}/{}'.format(account, app)

    @property
    def headers(self):
        headers = super().headers
        headers['User-Agent'] = self.app
        return headers

    def update(self):
        logger.debug('fetching GitHub project data')
        response = requests.get(
            self._url_builder('/repos/{repo}/commits', {'repo': self.repo}),
            headers=self.headers,
        )
        if response.status_code == 200:
            return self.format_data(self.repo, response.json())
        logger.error('failed to update GitHub project data')
        return {}

    @classmethod
    def format_data(cls, name, data):
        """Re-format the response data for the front-end.

        Arguments:
          data (:py:class:`list`): The JSON data from the response.
          name (:py:class:`str`): The name of the repository.

        Returns:
          :py:class:`dict`: The re-formatted data.

        """
        return dict(
            commits=[cls.format_commit(commit.get('commit', {}))
                     for commit in data[:5] or []],
            name=name,
        )

    @staticmethod
    def format_commit(commit):
        """Re-format the commit data for the front-end.

        Arguments:
          commit (:py:class:`dict`): The JSON data from the response.

        Returns:
          :py:class:`dict`: The re-formatted data.

        """
        author = commit.get('author', {}).get('name')
        committer = commit.get('committer', {}).get('name')
        if author is None:
            author_name = committer
        elif committer is None or author == committer:
            author_name = author
        else:
            author_name = '{} [{}]'.format(author, committer)
        return dict(
            author=author_name,
            committed=occurred(commit.get('committer', {}).get('date')),
            message=truncate(commit.get('message', '')),
        )
