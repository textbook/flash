import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.helpers import slow
from tests.integration.test_home_page import go_to_home_page


@pytest.mark.usefixtures('live_server')
@slow
def test_tracker_service_shows_velocity(selenium):
    go_to_home_page(selenium)
    WebDriverWait(selenium, 5).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, '.tracker-pane .velocity')
        )
    )
