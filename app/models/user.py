import time
import uuid
from http import HTTPStatus

import psycopg2  # type: ignore

from app.connections.user_db import connect
from app.models.country_enums import Country
from app.queries.user_queries import ADD_USER_QUERY
from app.queries.user_queries import GET_USER_BY_EMAIL_QUERY
from app.queries.user_queries import GET_USER_BY_ID_QUERY
from app.queries.user_queries import GET_USER_BY_USERNAME_QUERY


BASE = 64
INITIAL_TRADE_COUNT = 0
MILISECOND_OFFSET = 1000000


class User:
    """
    an object to house all data pertaining to a user.
    """

    def __init__(
        self,
        user_id: int,
        display_username: str,
        normalized_username: str,
        email: str,
        trade_count: int,
        home_location: Country,
        send_locations: list,
        created_at: int,
        # verification_token: str TODO Add back in once Google OAuth is set
    ) -> None:
        self.user_id = user_id
        self.display_username = display_username
        self.normalized_username = normalized_username
        self.email = email
        self.trade_count = trade_count
        self.home_location = home_location
        self.send_locations = send_locations
        self.created_at = created_at
        # self.verification_token = verification_token TODO Add back in once Google OAuth is set

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "display_username": self.display_username,
            "normalized_username": self.normalized_username,
            "email": self.email,
            "trade_count": self.trade_count,
            "home_location": self.home_location,
            "send_locations": self.send_locations,
            "created_at": self.created_at,
        }


def add_user(
    username: str,
    email: str,
    home_location: Country,
    send_locations: list,
) -> tuple[None | str, HTTPStatus]:
    """
    Function to handle insertion to DB.
    1. Pre-Work
        a) lowercase username
        b) verify lowercase username is available
        c) verify email is not in db
    2. Generate Base User Info
        a) generate id
        b) initialize User obj
    3. Add to DB
        a) excecute insert statement
        b) save and exit
    :param username: username of new user
    :param email: email of new user
    :param home_location: Country Enum where user resides
    :param send_locations: list of Country Enums that user will
    send to.
    :return: returns a tuple where the first item will be None
    if the user was successfully created or a string of the
    offending variable if not, and the second item will be the
    HTTPStatus code indicating success or failure reason
    """
    # 1. Pre-Work
    normalized_username = username.lower()
    conn = None

    try:
        conn = connect()

        if _is_existing_email(email, conn):
            return email, HTTPStatus.CONFLICT

        if _is_existing_username(normalized_username, conn):
            return username, HTTPStatus.CONFLICT

        # 2.a Generate Base User Info
        new_user_id = uuid.uuid4().int >> BASE
        created_at_time = time.time_ns() // MILISECOND_OFFSET

        # 2.b Generate User obj
        new_user = _build_user(
            (
                new_user_id,
                username,
                normalized_username,
                email,
                INITIAL_TRADE_COUNT,
                home_location,
                send_locations,
                created_at_time,
            )
        )

        # 3. Add to DB
        cur = conn.cursor()
        cur.execute(
            ADD_USER_QUERY.format(
                new_user.user_id,
                new_user.display_username,
                new_user.normalized_username,
                new_user.email,
                new_user.trade_count,
                new_user.home_location,
                new_user.send_locations,
                new_user.created_at,
            )
        )
        conn.commit()

    except Exception as error:
        print(error)
        return "internal error", HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if conn is not None:
            conn.close()
    return None, HTTPStatus.OK


def get_user_by_id(user_id: int) -> tuple[User | None, int]:
    """
    function to grab a user by id
    1. Verify ID
    2. Query DB
    3. Construct user obj
    """
    # 1. Verify ID
    if user_id is None:
        return None, HTTPStatus.BAD_REQUEST

    return_row = None
    conn = None

    # 2.Query Table
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(GET_USER_BY_ID_QUERY.format(user_id))

        # Grab first row (should only be one since user to user_id should be 1:1)
        return_row = cur.fetchone()

        cur.close()

    except Exception as error:
        print(error)  # TODO fail gracefully
        print("I failed somewhere")
        return None, HTTPStatus.NOT_FOUND

    finally:
        if conn is not None:
            conn.close()

    # 3.Construct user obj
    if return_row is None:
        return (None, HTTPStatus.NOT_FOUND)
    else:
        return _build_user(return_row), HTTPStatus.OK


def _is_existing_email(email: str, conn) -> bool:
    """
    Currently only used by add user to verify email does not exist
    on the platform
    """
    return_row = None
    cur = conn.cursor()

    cur.execute(GET_USER_BY_EMAIL_QUERY.format(email))

    return_row = cur.fetchone()

    cur.close()

    if return_row is None:
        return False
    else:
        return True


def _is_existing_username(username: str, conn) -> bool:
    """
    Currently only used by add user to verify username is
    not taken
    """
    return_row = None
    cur = conn.cursor()

    cur.execute(GET_USER_BY_USERNAME_QUERY.format(username))

    return_row = cur.fetchone()

    cur.close()

    if return_row is None:
        return False
    else:
        return True


def _build_user(user_tuple: tuple) -> User:
    return User(
        user_id=user_tuple[0],
        display_username=user_tuple[1],
        normalized_username=user_tuple[2],
        email=user_tuple[3],
        trade_count=user_tuple[4],
        home_location=user_tuple[5],
        send_locations=user_tuple[6],
        created_at=user_tuple[7],
        # verification_token = user_tuple[8],
    )
