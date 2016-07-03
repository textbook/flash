import pytest

slow = pytest.mark.skipif(
    not pytest.config.getoption('--runslow'),
    reason='need --runslow option to run',
)


def isexception(obj, exc=Exception):
    return isinstance(obj, type) and issubclass(obj, exc)


class Or:
    """Extends the Selenium expected conditions."""

    def __init__(self, *conds):
        self.conds = conds

    def __call__(self, driver):
        return any(cond(driver) for cond in self.conds)
