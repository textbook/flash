from datetime import datetime, timedelta
from unittest import mock

import pytest

from flash.services.utils import elapsed_time, occurred, truncate

TWO_DAYS_AGO = datetime.now() - timedelta(days=2, hours=12)


@pytest.mark.parametrize('input_, expected', [
    (('hello world',), 'hello world'),
    (('hello world', 10), 'hello w...'),
    (('hello world', 9), 'hello...'),
])
def test_truncate(input_, expected):
    assert truncate(*input_) == expected


@pytest.mark.parametrize('input_, expected, logged', [
    ((None,), 'time not available', True),
    ((TWO_DAYS_AGO.strftime('%Y-%m-%dT%H:%M:%SZ'),), '2 days ago', False),
    ((TWO_DAYS_AGO.strftime('%Y-%m-%dT%H:%M:%S'),), '2 days ago', False),
])
@mock.patch('flash.services.utils.logger.exception')
def test_occurred(exception, input_, expected, logged):
    assert occurred(*input_) == expected
    if logged:
        exception.assert_called_once_with('failed to parse occurrence time')
    else:
        exception.assert_not_called()


@pytest.mark.parametrize('input_, expected, logged', [
    ((None, None), 'elapsed time not available', True),
    (('2011-12-13T14:15:16', None), 'elapsed time not available', True),
    ((None, '2011-12-13T14:15:16'), 'elapsed time not available', True),
    (('2011-12-11T02:15:16', '2011-12-13T14:15:16'), 'took 2 days', False),
])
@mock.patch('flash.services.utils.logger.exception')
def test_elapsed_time(exception, input_, expected, logged):
    assert elapsed_time(*input_) == expected
    if logged:
        exception.assert_called_once_with('failed to generate elapsed time')
    else:
        exception.assert_not_called()
