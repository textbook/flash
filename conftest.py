import jinja2
import os
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


def pytest_collection_modifyitems(config, items):
    if config.getoption('--runslow'):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason='need --runslow option to run')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def jinja():
    here = os.path.dirname(__file__)
    template_path = '{}/flash/templates'.format(here)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
