import pytest

slow = pytest.mark.skipif(
    not pytest.config.getoption('--runslow'),
    reason='need --runslow option to run',
)


def isexception(obj, exc=Exception):
    return isinstance(obj, type) and issubclass(obj, exc)
