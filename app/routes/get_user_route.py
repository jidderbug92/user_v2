from flask import Blueprint
from flask import jsonify

from app.models.user import get_user_by_id


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """
    endpoint to return user info
    """
    user, status_code = get_user_by_id(user_id)
    if user is not None:
        user_dict = user.to_dict()

        return jsonify({str(user_id): user_dict}), status_code
    else:
        return jsonify({user_id: {}}), status_code


# Health check route
@user_blueprint.route("/health", methods=["GET"])
def health_check():
    # Return a JSON response with status and message
    return jsonify(status="healthy", message="Service is up and running"), 200
