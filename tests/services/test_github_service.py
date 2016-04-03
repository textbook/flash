from datetime import datetime, timedelta
from unittest import mock

import pytest

from flash.services.core import Service
from flash.services.github import GitHub


@pytest.fixture()
def service():
    return GitHub(api_token='foobar', account='foo', app='bar')


def test_tracker_service_type():
    assert issubclass(GitHub, Service)


def test_correct_config():
    assert GitHub.AUTH_PARAM == 'access_token'
    assert GitHub.REQUIRED == {'api_token', 'account', 'app'}
    assert GitHub.ROOT == 'https://api.github.com'
    assert GitHub.TEMPLATE == 'github'


TWO_DAYS_AGO = (datetime.now() - timedelta(days=2, hours=12)).strftime(
    '%Y-%m-%dT%H:%M:%SZ',
)


@mock.patch('flash.services.github.logger.debug')
@mock.patch('flash.services.github.requests.get', **{
    'return_value.status_code': 200,
    'return_value.json.return_value': [{'commit': {
        'author': {'name': 'alice'},
        'committer': {'name': 'bob', 'date': TWO_DAYS_AGO},
        'message': 'commit message',
    }}],
})
def test_update_success(get, debug, service):
    result = service.update()

    get.assert_called_once_with(
        'https://api.github.com/repos/foo/bar/commits?access_token=foobar',
        headers={'User-Agent': 'bar'}
    )
    debug.assert_called_once_with('fetching GitHub project data')
    assert result == {'commits': [{
        'message': 'commit message',
        'author': 'alice [bob]',
        'committed': '2 days ago'
    }], 'name': 'foo/bar'}


@mock.patch('flash.services.github.logger.error')
@mock.patch('flash.services.github.requests.get', **{
    'return_value.status_code': 401,
})
def test_update_failure(get, error, service):
    result = service.update()

    get.assert_called_once_with(
        'https://api.github.com/repos/foo/bar/commits?access_token=foobar',
        headers={'User-Agent': 'bar'}
    )
    error.assert_called_once_with('failed to update GitHub project data')
    assert result == {}

