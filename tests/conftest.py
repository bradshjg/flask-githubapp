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

    @github_app.on('issues.edited')
    def test_issue_edited():
        return 'issue edited action'

    @github_app.on('push')
    def test_push():
        return 'push event'

    return app
