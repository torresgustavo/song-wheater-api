from flask import Flask
from application.weather import wheather_bp


def register_blueprint(app: Flask):
    app.register_blueprint(wheather_bp)
