from unittest import mock

import pytest

from flash import services


def test_define_services_missing():
    with mock.patch.dict(services.SERVICES, {}, clear=True):
        with pytest.raises(ValueError):
            services.define_services({'anything': None})


def test_define_services_present():
    mock_service = mock.MagicMock()
    present = {'present': mock_service}
    expected = {'present': mock_service.return_value}

    with mock.patch.dict(services.SERVICES, present, clear=True):
        result = services.define_services({'present': {'foo': 'bar'}})

    assert result == expected
    mock_service.assert_called_once_with(foo='bar')
