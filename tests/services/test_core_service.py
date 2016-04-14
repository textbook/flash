from collections import OrderedDict
from datetime import datetime

import pytest

from flash.services.core import Service


class Test(Service):

    REQUIRED = {'foo', 'bar'}
    ROOT = 'root/url'

    def __init__(self):
        super().__init__()

    def update(self):
        pass


def test_core_is_abstract():
    with pytest.raises(TypeError):
        Service()


@pytest.mark.parametrize('config', [
    ({},),
    ({'foo': None},),
    ({'bar': None},),
])
def test_required_config(config):
    with pytest.raises(TypeError):
        Test.from_config(**config)


@pytest.mark.parametrize('input_, expected', [
    (('/endpoint',), 'root/url/endpoint'),
    (('/endpoint/{foo}', {'foo': 'bar'}), 'root/url/endpoint/bar'),
    (('/endpoint', {}, {'foo': 'bar'}), 'root/url/endpoint?foo=bar'),
    (
        ('/endpoint', {}, OrderedDict([('foo', 'bar'), ('bar', 'baz')])),
        'root/url/endpoint?foo=bar&bar=baz',
    ),
    (
        (
                '/endpoint/{hello}',
                {'hello': 'world'},
                OrderedDict([('foo', 'bar'), ('bar', 'baz')]),
        ),
        'root/url/endpoint/world?foo=bar&bar=baz',
    ),
])
def test_url_builder(input_,expected):
    assert Test().url_builder(*input_) == expected


def test_build_estimate_unstarted():
    current = {'started_at': None}

    Service.estimate_time(current, [])

    assert current['elapsed'] == 'estimate not available'


def test_build_estimate_no_history():
    current = {'started_at': 123456789}

    Service.estimate_time(current, [])

    assert current['elapsed'] == 'estimate not available'


def test_build_estimate_usable():
    current = {'started_at': int(datetime.now().timestamp())}
    previous = [
        {'outcome': 'passed', 'duration': 610},
        {'outcome': 'passed', 'duration': 600},
        {'outcome': 'passed', 'duration': 605},
    ]

    Service.estimate_time(current, previous)

    assert current['elapsed'] == 'ten minutes left'


