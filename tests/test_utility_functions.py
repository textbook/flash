from datetime import datetime
from unittest import mock

from flash.flash import CACHE, parse_config, update_service

CONFIG_STRING = '{"name":"foo","services":[]}'


@mock.patch('flash.flash.define_services')
@mock.patch('flash.flash.getenv', return_value=CONFIG_STRING)
@mock.patch('flash.flash.logger')
def test_parse_config_from_env(logger, getenv, define_services):
    result = parse_config()

    assert result == {
        'name': 'foo',
        'project_name': 'unnamed',
        'services': define_services.return_value,
        'style': 'default',
    }
    getenv.assert_called_once_with('FLASH_CONFIG')
    logger.info.assert_called_once_with(
        'loading configuration from environment',
    )
    define_services.assert_called_once_with([])


@mock.patch('flash.flash.open', mock.mock_open(read_data=CONFIG_STRING))
@mock.patch('flash.flash.define_services')
@mock.patch('flash.flash.getenv', return_value=None)
@mock.patch('flash.flash.logger')
def test_parse_config_from_file(logger, getenv, define_services):
    result = parse_config()

    assert result == {
        'name': 'foo',
        'project_name': 'unnamed',
        'services': define_services.return_value,
        'style': 'default',
    }
    getenv.assert_called_once_with('FLASH_CONFIG')
    logger.info.assert_called_once_with('loading configuration from file')
    define_services.assert_called_once_with([])


@mock.patch('flash.flash.open', mock.mock_open(read_data="""
{
  "project_name": "demo",
  "services": [
    {
      "name": "tracker",
      "api_token": "$TRACKER_API_TOKEN",
      "project_id": "$TRACKER_PROJECT_ID"
    }
  ]
}
"""))
@mock.patch('flash.flash.define_services')
@mock.patch('flash.flash.getenv', side_effect=dict(
    FLASH_CONFIG=None,
    TRACKER_API_TOKEN='password',
    TRACKER_PROJECT_ID='123',
).get)
def test_parse_config_env_vars(getenv, define_services):
    result = parse_config()
    define_services.assert_called_once_with([
        dict(name='tracker', api_token='password', project_id='123')
    ])
    getenv.assert_has_calls(
        [
            mock.call('FLASH_CONFIG'),
            mock.call('TRACKER_API_TOKEN', '$TRACKER_API_TOKEN'),
            mock.call('TRACKER_PROJECT_ID', '$TRACKER_PROJECT_ID'),
        ],
        any_order=True  # dictionary ordering
    )


@mock.patch('flash.flash.logger')
def test_update_service_not_found(logger):
    result = update_service('foo', {})

    assert result == {}
    logger.warning.assert_called_once_with('service not found: %s', 'foo')


@mock.patch('flash.flash.logger')
def test_update_no_result(logger):
    mock_service = mock.MagicMock(**{'update.return_value': None})

    result = update_service('foo', {'foo': mock_service})

    assert result == {}
    logger.warning.assert_called_once_with(
        'no data received for service: %s',
        'foo',
    )
    mock_service.update.assert_called_once_with()


@mock.patch('flash.flash.logger')
def test_update_result(logger):
    mock_result = {'foo': 'bar'}
    mock_service = mock.MagicMock(**{'update.return_value': mock_result})

    result = update_service('foo', {'foo': mock_service})

    assert result == mock_result
    logger.warning.assert_not_called()
    mock_service.update.assert_called_once_with()


@mock.patch.dict(CACHE, {'foo': {
    'data': {'foo': 'bar'},
    'updated': datetime(2011, 12, 13, 14, 15, 16),
}}, clear=True)
def test_update_cached():
    mock_service = mock.MagicMock(**{'update.return_value': None})

    result = update_service('foo', {'foo': mock_service})

    assert result == {'foo': 'bar', 'last_updated': '2011-12-13'}
    mock_service.update.assert_called_once_with()
