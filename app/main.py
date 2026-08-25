from flask import Flask

from app.routes.get_user_route import user_blueprint


app = Flask(__name__)

app.register_blueprint(user_blueprint, url_prefix="/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
