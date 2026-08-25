ADD_USER_QUERY = """INSERT INTO users(user_id, display_username, normalized_username, email, trade_count, home_location, send_locations, created_at)
VALUES({}, '{}', '{}', '{}', {}, '{}', ARRAY{}, {});"""

GET_USER_BY_ID_QUERY = """
    SELECT *
    FROM users
    WHERE user_id = {};
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT *
    FROM users
    WHERE email = '{}';
"""

GET_USER_BY_USERNAME_QUERY = """
    SELECT *
    FROM users
    WHERE normalized_username = '{}';
"""
