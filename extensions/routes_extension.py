from flask import Flask
from application.weather.controllers.v1 import weather_bp


def register_blueprint(app: Flask):
    app.register_blueprint(weather_bp)
