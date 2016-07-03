from flask import url_for
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.helpers import slow


@pytest.mark.usefixtures('live_server')
@slow
def test_scratchpad_accessible(selenium):
    go_to_scratchpad(selenium)
    WebDriverWait(selenium, 5).until(expected_conditions.title_is(
        'Flask + Dashboard = Flash'
    ))
    assert selenium.find_element(By.CLASS_NAME, 'flash-project-name').text.upper() == 'SCRATCHPAD'


def go_to_scratchpad(selenium):
    selenium.get(url_for('scratchpad', _external=True))
