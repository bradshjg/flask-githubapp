import pytest

from flask import Flask


@pytest.fixture
def app():
    app = Flask('test_app')
    app.config['GITHUBAPP_ID'] = 1
    app.config['GITHUBAPP_KEY'] = 'key'
    app.config['GITHUBAPP_SECRET'] = 'secret'
    return app