from datetime import datetime
from unittest import mock

from flash.flash import CACHE, update_service


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
