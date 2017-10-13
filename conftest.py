import pytest

import flash

@pytest.fixture
def app():
    return flash.app


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return chrome_options


def pytest_addoption(parser):
    parser.addoption('--runslow', action='store_true', help='run slow tests')
