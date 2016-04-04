from collections import OrderedDict

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
