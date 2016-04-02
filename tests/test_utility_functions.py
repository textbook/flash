from unittest import mock

from flash.flash import parse_config, update_service

CONFIG_STRING = '{"name":"foo","services":[]}'


@mock.patch('flash.flash.define_services')
@mock.patch('flash.flash.getenv', return_value=CONFIG_STRING)
@mock.patch('flash.flash.logger')
def test_parse_config_from_env(logger, getenv, define_services):
    result = parse_config()

    assert result == {'name': 'foo', 'services': define_services.return_value}
    getenv.assert_called_once_with('FLASH_CONFIG')
    logger.info.assert_called_once_with(
        'loading configuration from environment',
    )
    define_services.assert_called_once_with([])


@mock.patch('flash.flash.open', mock.mock_open(read_data=CONFIG_STRING))
@mock.patch('flash.flash.define_services')
@mock.patch('flash.flash.getenv', return_value=None)
@mock.patch('flash.flash.logger')
def test_parse_config_from_env(logger, getenv, define_services):
    result = parse_config()

    assert result == {'name': 'foo', 'services': define_services.return_value}
    getenv.assert_called_once_with('FLASH_CONFIG')
    logger.info.assert_called_once_with('loading configuration from file')
    define_services.assert_called_once_with([])


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
