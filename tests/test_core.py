from flask_githubapp import GitHubApp

from github3 import GitHub, GitHubEnterprise


def test_default_config(app):
    """make sure we're casting things that make sense to cast"""
    github_app = GitHubApp(app)
    with app.app_context():
        assert github_app.id == 1
        assert github_app.key == b'key'
        assert github_app.secret == b'secret'


def test_init_app(app):
    github_app = GitHubApp()
    github_app.init_app(app)
    assert app.config['GITHUBAPP_API_URL'] == 'https://api.github.com'


def test_github_client(app):
    github_app = GitHubApp(app)
    with app.app_context():
        assert isinstance(github_app.client, GitHub)


def test_github_enterprise_client(app):
    enterprise_url = 'https://enterprise.github.com'
    app.config['GITHUBAPP_API_URL'] = enterprise_url
    github_app = GitHubApp(app)
    with app.app_context():
        assert isinstance(github_app.client, GitHubEnterprise)
        assert github_app.client.url == enterprise_url
