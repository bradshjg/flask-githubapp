import base64
import json
import os
import pathlib
from typing import Any

import pytest
from app import create_app


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["GITHUBAPP_ID"] = "some-app-id"
    os.environ["GITHUBAPP_KEY_B64"] = base64.b64encode(b"some-base-64-private-key").decode()
    os.environ["GITHUBAPP_SECRET"] = "secret"


@pytest.fixture
def app():
    return create_app(test_config={"TESTING": True, "GITHUBAPP_SECRET": False})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def load_fixture():
    def loader(fixture_name: str) -> dict[str, Any]:
        fixtures_dir = pathlib.Path(__file__).parent / "fixtures"
        with open(fixtures_dir / f"{fixture_name}.json") as fp:
            return json.load(fp)

    return loader
