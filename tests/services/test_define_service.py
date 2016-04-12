import pytest

from flash.services import define_services


def test_define_service_failed():
    with pytest.raises(ValueError):
        define_services([{'name': 'garbage'}])
