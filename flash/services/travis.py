"""Defines the Travis CI service integrations."""

import logging

import requests

from .core import Service
from .utils import health_summary, naturaldelta, truncate

logger = logging.getLogger(__name__)


class TravisOS(Service):
    """Show the current status of an open-source project.

    Arguments:
      account (:py:class:`str`): The name of the account.
      app (:py:class:`str`): The name of the application.

    Attributes:
      repo (:py:class:`str`): The repository name, in the format
        ``account/application``.

    """

    OUTCOMES = {
        'canceled': 'cancelled',
        'created': 'working',
        'failed': 'failed',
        'passed': 'passed',
        'started': 'working',
        '?': 'crashed',
    }
    REQUIRED = {'account', 'app'}
    ROOT = 'https://api.travis-ci.org'
    TEMPLATE = 'travis'

    def __init__(self, *, account, app, **kwargs):
        super().__init__(**kwargs)
        self.account = account
        self.app = app
        self.repo = '{}/{}'.format(account, app)

    @property
    def headers(self):
        headers = super().headers
        headers.update({
            'Accept': 'application/vnd.travis-ci.2+json',
            'User-Agent': 'Flash',
        })
        return headers

    def update(self):
        logger.debug('fetching Travis CI project data')
        response = requests.get(
            self.url_builder('/repos/{repo}/builds', {'repo': self.repo}),
            headers=self.headers,
        )
        if response.status_code == 200:
            return self.format_data(response.json())
        logger.error('failed to update Travis CI project data')
        return {}

    def format_data(self, data):
        """Re-format the response data for the front-end.

        Arguments:
          data (:py:class:`dict`): The JSON data from the response.

        Returns:
          :py:class:`dict`: The re-formatted data.

        """
        commits = {commit['id']: commit for commit in data.get('commits', [])}
        builds = [
            self.format_build(build, commits.get(build.get('commit_id'), {}))
            for build in data.get('builds', [])[:5]
        ]
        return dict(
            builds=builds,
            health=health_summary(builds),
            name=self.repo,
        )

    @classmethod
    def format_build(cls, build, commit):
        """Re-format the build and commit data for the front-end.

        Arguments:
          build (:py:class:`dict`): The build data from the response.
          commit (:py:class:`dict`): The commit data from the response.

        Returns:
          :py:class:`dict`: The re-formatted data.

        """
        status = build.get('state')
        if status not in cls.OUTCOMES:
            logger.warning('unknown status: %s', status)
        try:
            elapsed = 'took {}'.format(naturaldelta(int(build.get('duration'))))
        except (TypeError, ValueError):
            logger.exception('failed to generate elapsed time')
            elapsed = 'elapsed time not available'
        return dict(
            author=commit.get('author_name'),
            elapsed=elapsed,
            message=truncate(commit.get('message', '')),
            outcome=cls.OUTCOMES.get(status),
        )
