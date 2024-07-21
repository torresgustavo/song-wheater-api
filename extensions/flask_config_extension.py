import os
from flask import Flask, Response, json
from werkzeug.exceptions import HTTPException


from configs.config import DevelopmentConfig, TestingConfig, ProductionConfig
from domain.shared.errors.forbidden_error import ForbiddenError
from domain.shared.errors.not_found_error import NotFoundError
from domain.shared.errors.to_many_requests_error import ToManyRequestsError
from domain.shared.errors.unauthorized_error import UnauthorizedError
from domain.shared.errors.unexpected_client_error import UnexpectedClientError


def register_config(app: Flask):
    __register_config_by_enviroment(app)
    __register_error_handle(app)


def __register_config_by_enviroment(app: Flask):
    app_mode = os.getenv("FLASK_ENV", "development")

    if app_mode == "production":
        app.config.from_object(ProductionConfig())
    elif app_mode == "testing":
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())


def __register_error_handle(app: Flask):
    def __format_exception_data_to_response(exception_data: dict) -> Response:
        return Response(
            response=json.dumps(exception_data),
            status=exception_data["status_code"],
            content_type="application/json",
            mimetype="application/json",
        )

    @app.errorhandler(ForbiddenError)
    def handle_forbidden_error(error: ForbiddenError) -> Response:
        exception_data = {
            "message": error.message,
            "detail": error.detail,
            "error_code": error.error_code,
            "status_code": 403,
        }

        return __format_exception_data_to_response(exception_data)

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error: NotFoundError) -> Response:
        exception_data = {
            "message": error.message,
            "detail": error.detail,
            "error_code": error.error_code,
            "status_code": 404,
        }

        return __format_exception_data_to_response(exception_data)

    @app.errorhandler(ToManyRequestsError)
    def handle_to_many_requests_error(error: ToManyRequestsError) -> Response:
        exception_data = {
            "message": error.message,
            "detail": error.detail,
            "error_code": error.error_code,
            "status_code": 429,
        }

        return __format_exception_data_to_response(exception_data)

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized_error(error: UnauthorizedError) -> Response:
        exception_data = {
            "message": error.message,
            "detail": error.detail,
            "error_code": error.error_code,
            "status_code": 401,
        }

        return __format_exception_data_to_response(exception_data)

    @app.errorhandler(UnexpectedClientError)
    def handle_unexpected_error(error: UnexpectedClientError) -> Response:
        exception_data = {
            "message": error.message,
            "detail": error.detail,
            "error_code": error.error_code,
            "status_code": 500,
        }

        return __format_exception_data_to_response(exception_data)

    @app.errorhandler(Exception)
    def handle_http_exception(error: HTTPException) -> Response:
        exception_data = {
            "message": error.description,
            "detail": None,
            "error_code": None,
            "status_code": error.code,
        }

        return __format_exception_data_to_response(exception_data)
