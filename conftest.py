import os
import pytest

from flask import Flask

from app import create_app


@pytest.fixture(autouse=True)
def app():
    os.environ["FLASK_ENV"] = "testing"

    app = create_app()

    yield app


@pytest.fixture(autouse=True)
def client(app: Flask):
    with app.test_client() as client:
        yield client
