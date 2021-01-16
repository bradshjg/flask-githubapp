import pytest

from flask import Flask

from flask_githubapp import GitHubApp


@pytest.fixture
def app():
    app = Flask('test_app')
    app.config['GITHUBAPP_ID'] = 1
    app.config['GITHUBAPP_KEY'] = 'key'
    app.config['GITHUBAPP_SECRET'] = 'secret'
    return app

@pytest.fixture
def github_app(app):
    github_app = GitHubApp(app)

    @github_app.on('issues')
    def test_issue():
        return 'issue event'

    @github_app.on('issues.opened')
    def test_issue_opened():
        return 'issue opened action'
    return app
