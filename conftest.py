import pytest

import flash

@pytest.fixture
def app():
    return flash.app


def pytest_addoption(parser):
    parser.addoption('--runslow', action='store_true', help='run slow tests')
