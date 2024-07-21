from flask import Flask
from application.music.controllers.v1 import music_bp


def register_blueprint(app: Flask):
    app.register_blueprint(music_bp)
