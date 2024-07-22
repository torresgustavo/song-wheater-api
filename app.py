from flask import Flask
from extensions.cache_extension import register_cache
from extensions.flask_config_extension import register_config
from extensions.routes_extension import register_blueprint


def create_app() -> Flask:
    app = Flask(__name__)

    register_config(app)
    register_blueprint(app)
    register_cache(app)

    return app
