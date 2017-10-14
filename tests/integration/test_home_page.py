from flask import url_for
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.helpers import slow, Or


@pytest.mark.usefixtures('live_server')
@slow
def test_home_page_accessible(selenium):
    go_to_home_page(selenium)
    WebDriverWait(selenium, 5).until(expected_conditions.title_is(
        'Flask + Dashboard = Flash'
    ))
    assert selenium.find_element(By.CLASS_NAME, 'flash-project-name').text.upper() == 'DEMO'


@pytest.mark.usefixtures('live_server')
@slow
def test_home_page_contains_travis_status(selenium):
    go_to_home_page(selenium)
    WebDriverWait(selenium, 5).until(
        expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, 'travis-pane')
        )
    )


@pytest.mark.usefixtures('live_server')
@slow
def test_home_page_contains_countdown(selenium):
    go_to_home_page(selenium)
    spec = By.ID, 'ending'
    WebDriverWait(selenium, 5).until(Or(
        expected_conditions.text_to_be_present_in_element(spec, 'in'),
        expected_conditions.text_to_be_present_in_element(spec, 'ago'),
    ))
    countdown = selenium.find_element(*spec).text.lower()
    assert 'in' in countdown or 'ago' in countdown
    assert countdown.startswith('project ends')


@pytest.mark.usefixtures('live_server')
@slow
def test_home_page_data_prefilled(selenium):
    go_to_home_page(selenium)
    elements = selenium.find_elements(By.CLASS_NAME, 'message')
    assert [element.text for element in elements] != ['', '', '', '']


def go_to_home_page(selenium):
    selenium.get(url_for('home', _external=True))
