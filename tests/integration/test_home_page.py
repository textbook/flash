from flask import url_for
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.helpers import slow


@pytest.mark.usefixtures('live_server')
@slow
def test_home_page_accessible(selenium):
    go_to_home_page(selenium)
    WebDriverWait(selenium, 5).until(expected_conditions.title_is(
        'Flask + Dashboard = Flash'
    ))
    assert selenium.find_element(By.CLASS_NAME, 'headline').text == 'PROJECT GNOME'


@pytest.mark.usefixtures('live_server')
@slow
def test_home_page_contains_tracker_dashboard(selenium):
    go_to_home_page(selenium)
    WebDriverWait(selenium, 5).until(
        expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, 'tracker-pane')
        )
    )


def go_to_home_page(selenium):
    selenium.get(url_for('home', _external=True))
