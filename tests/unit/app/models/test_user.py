from unittest import mock

import psycopg2

from app.models.country_enums import Country
from app.models.user import add_new_user
from app.models.user import get_user_by_id
from app.models.user import User


@mock.patch("psycopg2.connect")
def test_add_new_user_ok(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = None

    resp1, resp2 = add_new_user(
        "testusername",
        "testeamil@test.com",
        Country.UNITED_STATES,
        [Country.UNITED_STATES, Country.CANADA],
    )

    assert resp1 == None
    assert resp2 == 200


@mock.patch("psycopg2.connect")
def test_add_new_user_existing_user(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {}

    resp1, resp2 = add_new_user(
        "testusername",
        "testemail@test.com",
        Country.UNITED_STATES,
        [Country.UNITED_STATES, Country.CANADA],
    )

    assert resp1 == "testemail@test.com"
    assert resp2 == 409


@mock.patch("psycopg2.connect")
def test_get_user_by_id_ok(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = (
        0,
        "testUsername",
        "testusername",
        "testemail@test.com",
        100,
        Country.UNITED_STATES,
        [Country.UNITED_STATES, Country.CANADA],
        1205215631,
    )

    resp1, resp2 = get_user_by_id(0)

    assert resp1.email == "testemail@test.com"
    assert resp2 == 200
