from http import HTTPStatus

from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask import request

from app.models.user import add_new_user


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/add_user/<int:user_id>", methods=["POST"])
def add_user():
    data = request.get_json()

    if data is None:
        return {"error": "No data recieved"}

    error, status = add_user(
        data["username"], data["email"], data["home_loc"], data["send_loc"]
    )

    return jsonify(status=status, error=error)
