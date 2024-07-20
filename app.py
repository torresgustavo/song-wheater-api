from flask import Flask
from extensions.flask_config_extension import register_config
from extensions.routes_extension import register_blueprint

# from extensions.injector_extension import register_dependency_injection
# from extensions.exception_extension import register_exception_handler


def create_app() -> Flask:
    app = Flask(__name__)

    register_config(app)
    register_blueprint(app)

    # register_exception_handler(app)
    # register_dependency_injection(app)
    return app
