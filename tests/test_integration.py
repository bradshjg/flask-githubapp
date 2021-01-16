import os

FIXURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fixtures'
)


def test_issues_hook_valid_legacy_signature(github_app):
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature': 'sha1=85d20eda7a4e518f956b99f432b1225de8516e56'
                           })
        assert resp.status_code == 200

def test_issues_hook_valid_signature(github_app):
    """a valid webhook w/ signature should return a 200 response with a valid response payload"""
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature-256': 'sha256=a4adf8a7da6573f0fbb2f9d43dbe07c7c2e91d27f6ad65bdafae233a88ec0e4b'
                           })
        assert resp.status_code == 200
        assert resp.json == {'calls': {'test_issue': 'issue event', 'test_issue_opened': 'issue opened action'}, 'status': 'HIT'}


def test_issues_hook_invalid_legacy_signature(github_app):
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature': 'sha1=badhash'
                           })
        assert resp.status_code == 400


def test_issues_hook_invalid_signature(github_app):
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature': 'sha256=badhash'
                           })
        assert resp.status_code == 400


def test_issues_hook_missing_signature(github_app):
    """Return 400 response if the signature is missing and verification is enabled"""
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                           })
        assert resp.status_code == 400


def test_issues_hook_verification_disabled_missing_signature(github_app):
    """Return 200 response and valid payload if the signature is missing and verification has been disabled"""
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    github_app.config['GITHUBAPP_SECRET'] = False

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                           })
        assert resp.status_code == 200
        assert resp.json == {'calls': {'test_issue': 'issue event', 'test_issue_opened': 'issue opened action'}, 'status': 'HIT'}
