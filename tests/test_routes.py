from http import HTTPStatus

from flask import url_for


def test_home_route(client):
    response = client.get(url_for('home'))
    assert response.status_code == HTTPStatus.OK


def test_service_route(client):
    response = client.get(url_for('services'))
    assert response.status_code == HTTPStatus.OK


def test_scratchpad_route(client):
    response = client.get(url_for('scratchpad'))
    assert response.status_code == HTTPStatus.OK
