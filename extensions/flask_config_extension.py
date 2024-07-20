import os
from flask import Flask

from configs.config import DevelopmentConfig, TestingConfig, ProductionConfig


def register_config(app: Flask):
    app_mode = os.getenv("FLASK_ENV", "development")

    if app_mode == "production":
        app.config.from_object(DevelopmentConfig())
    elif app_mode == "testing":
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())
