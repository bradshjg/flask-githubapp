import os

from flask_githubapp import GitHubApp

FIXURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fixtures'
)


def test_issues_hook_valid_signature(app):
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    GitHubApp(app)

    with app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature': 'sha1=85d20eda7a4e518f956b99f432b1225de8516e56'
                           })
        assert resp.status_code == 200


def test_issues_hook_invalid_signature(app):
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    GitHubApp(app)

    with app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature': 'sha1=badhash'
                           })
        assert resp.status_code == 400
