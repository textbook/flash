import json
from os import path
from unittest import mock

import pytest

from flash.parse import parse_config, _read_file


CONFIG_STRING = '{"name":"foo","services":[]}'


@mock.patch('flash.parse.define_services')
@mock.patch('flash.parse.getenv', return_value=CONFIG_STRING)
@mock.patch('flash.parse.logger')
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


@mock.patch.object(path, 'join', return_value='some/file/path')
@mock.patch('flash.parse._read_file', return_value=json.loads(CONFIG_STRING))
@mock.patch('flash.parse.define_services')
@mock.patch('flash.parse.getenv', return_value=None)
@mock.patch('flash.parse.logger')
def test_parse_config_from_file(logger, getenv, define_services, mock_read, _):
    result = parse_config()

    assert result == {
        'name': 'foo',
        'project_name': 'unnamed',
        'services': define_services.return_value,
        'style': 'default',
    }
    getenv.assert_called_once_with('FLASH_CONFIG')
    logger.info.assert_called_once_with(
        'loading configuration from file: %r',
        'some/file/path',
    )
    define_services.assert_called_once_with([])
    mock_read.assert_called_once_with(path.join.return_value)


@mock.patch('flash.parse.open', mock.mock_open(read_data="""
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
@mock.patch('flash.parse.define_services')
@mock.patch('flash.parse.getenv', side_effect=dict(
    FLASH_CONFIG=None,
    TRACKER_API_TOKEN='password',
    TRACKER_PROJECT_ID='123',
).get)
def test_parse_config_env_vars(getenv, define_services):
    _ = parse_config()
    define_services.assert_called_once_with([
        dict(name='tracker', api_token='password', project_id='123')
    ])
    getenv.assert_has_calls(
        [
            mock.call('FLASH_CONFIG'),
            mock.call('TRACKER_API_TOKEN'),
            mock.call('TRACKER_PROJECT_ID'),
        ],
        any_order=True  # dictionary ordering
    )


@mock.patch('flash.parse.open', mock.mock_open(read_data="""
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
def test_read_file():
    assert _read_file('some/file/name') == dict(
        project_name='demo',
        services=[dict(
            name='tracker',
            api_token='$TRACKER_API_TOKEN',
            project_id='$TRACKER_PROJECT_ID',
        )],
    )


@mock.patch.object(path, 'join', return_value='some/file/path')
@mock.patch('flash.parse._read_file', side_effect=FileNotFoundError)
@mock.patch('flash.parse.define_services')
@mock.patch('flash.parse.getenv', return_value=None)
@mock.patch('flash.parse.logger')
def test_missing_file(logger, getenv, define_services, mock_read, _):
    with pytest.raises(SystemExit):
        parse_config()

    getenv.assert_called_once_with('FLASH_CONFIG')
    logger.error.assert_called_once_with(
        'no configuration available, set FLASH_CONFIG or provide config.json'
    )
    define_services.assert_not_called()
    mock_read.assert_called_once_with('some/file/path')


@mock.patch(
    'flash.parse._read_file',
    return_value=dict(project_name='test', services=[dict(name='demo', token='$ENV_VAR')]),
)
@mock.patch('flash.parse.define_services')
@mock.patch('flash.parse.getenv', return_value=None)
@mock.patch('flash.parse.logger')
def test_missing_env_var(logger, getenv, define_services, _):
    result = parse_config()

    assert result == {
        'project_name': 'test',
        'services': define_services.return_value,
        'style': 'default',
    }
    getenv.assert_has_calls(
        [
            mock.call('FLASH_CONFIG'),
            mock.call('ENV_VAR'),
        ],
        any_order=True  # dictionary ordering
    )
    logger.warning.assert_called_once_with(
        'environment variable %r not found',
        'ENV_VAR',
    )
    define_services.assert_called_once_with([dict(name='demo', token='$ENV_VAR')])
