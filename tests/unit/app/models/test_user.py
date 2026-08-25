from unittest import mock

import psycopg2

from app.models.country_enums import Country
from app.models.user import add_user
from app.models.user import User


@mock.patch("psycopg2.connect")
def test_add_user_ok(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = None

    resp1, resp2 = add_user(
        "testusername",
        "testeamil@test.com",
        Country.UNITED_STATES,
        [Country.UNITED_STATES, Country.CANADA],
    )

    assert resp1 == None
    assert resp2 == 200


@mock.patch("psycopg2.connect")
def test_add_user_existing_user(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {}

    resp1, resp2 = add_user(
        "testusername",
        "testemail@test.com",
        Country.UNITED_STATES,
        [Country.UNITED_STATES, Country.CANADA],
    )

    assert resp1 == "testemail@test.com"
    assert resp2 == 409
