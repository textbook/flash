from unittest import mock

import pytest

from flash.services.core import Service
from flash.services.tracker import Tracker


@pytest.fixture()
def service():
    return Tracker(api_token='foobar', project_id=123)


def test_tracker_service_type():
    assert issubclass(Tracker, Service)


def test_correct_config():
    assert Tracker.TEMPLATE == 'tracker'
    assert Tracker.REQUIRED == {'api_token', 'project_id'}
    assert Tracker.ROOT == 'https://www.pivotaltracker.com/services/v5'


def test_headers(service):
    assert service.headers == {'X-TrackerToken': 'foobar'}


@mock.patch('flash.services.tracker.requests.get', **{
    'return_value.status_code': 200,
    'return_value.json.return_value': {'velocity': 10},
})
def test_get_velocity_success(get, service):
    data = {'current_iteration_number': 456}

    service._get_velocity(data)

    get.assert_called_once_with(
        ('https://www.pivotaltracker.com/services/v5/projects/123/'
         'iterations/456?fields=:default,velocity'),
        headers={'X-TrackerToken': 'foobar'},
    )
    assert data == {'current_iteration_number': 456, 'velocity': 10}


@mock.patch('flash.services.tracker.logger.debug')
@mock.patch('flash.services.tracker.requests.get', **{
    'return_value.status_code': 200,
    'return_value.headers': {'X-Tracker-Project-Version': '1'},
    'return_value.json.return_value': {'foo': 'bar'},
})
def test_update_success(get, debug, service):
    service.project_version = 2
    service._cached = {'foo': 'bar'}

    result = service.update()

    get.assert_called_once_with(
        'https://www.pivotaltracker.com/services/v5/projects/123',
        headers={'X-TrackerToken': 'foobar'},
    )
    debug.assert_called_once_with('fetching Tracker project data')
    assert result == {'foo': 'bar'}


@mock.patch('flash.services.tracker.logger.error')
@mock.patch('flash.services.tracker.requests.get', **{
    'return_value.status_code': 401,
})
def test_get_velocity_failure(get, error, service):
    data = {'current_iteration_number': 456}

    service._get_velocity(data)

    get.assert_called_once_with(
        ('https://www.pivotaltracker.com/services/v5/projects/123/'
         'iterations/456?fields=:default,velocity'),
        headers={'X-TrackerToken': 'foobar'},
    )
    assert data == {'current_iteration_number': 456}
    error.assert_called_once_with('failed to update project velocity')


@mock.patch('flash.services.tracker.logger.error')
@mock.patch('flash.services.tracker.requests.get', **{
    'return_value.status_code': 401,
})
def test_update_failure(get, error, service):
    result = service.update()

    get.assert_called_once_with(
        'https://www.pivotaltracker.com/services/v5/projects/123',
        headers={'X-TrackerToken': 'foobar'},
    )
    error.assert_called_once_with('failed to update Tracker project data')
    assert result == {}
