import pytest

from flash import flash


@pytest.fixture
def app():
    return flash.flask_app


def pytest_addoption(parser):
    parser.addoption('--runslow', action='store_true', help='run slow tests')
