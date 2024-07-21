import os
import pytest

from app import create_app


@pytest.fixture(autouse=True)
def app():
    os.environ["FLASK_ENV"] = "testing"

    app = create_app()

    yield app
