import pytest

from flash.services import define_services


@pytest.mark.parametrize('input_', [
    [{'name': 'garbage'}],
    [
        {'name': 'codeship', 'api_token': 'foo', 'project_id': 'bar'},
        {'name': 'codeship'},
    ],
])
def test_define_service_failed(input_):
    with pytest.raises(ValueError):
        define_services(input_)
