import os

FIXURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fixtures'
)


def test_issues_hook_valid_legacy_signature(github_app):
    """a valid webhook w/ legacy signature should return a 200 response with a valid response payload"""
    with open(os.path.join(FIXURES_DIR, 'issues_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'issues',
                               'X-Hub-Signature': 'sha1=ad68425a164a7a06d4849a63163f15656810175b'
                           })
        assert resp.status_code == 200
        assert resp.json == {'calls': {'test_issue': 'issue event', 'test_issue_edited': 'issue edited action'},
                             'status': 'HIT'}

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
                               'X-Hub-Signature-256': 'sha256=5700c0515bec05804df657c3ebbf5f9585701a9f0a2a5633ca2d6dbd375a63a2'
                           })
        assert resp.status_code == 200
        assert resp.json == {'calls': {'test_issue': 'issue event', 'test_issue_edited': 'issue edited action'}, 'status': 'HIT'}


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
        assert resp.json == {'calls': {'test_issue': 'issue event', 'test_issue_edited': 'issue edited action'}, 'status': 'HIT'}

def test_hook_without_action(github_app):
    """Return a 200 response and valid payload for hooks without an action key"""
    with open(os.path.join(FIXURES_DIR, 'push_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    github_app.config['GITHUBAPP_SECRET'] = False

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'push',
                           })
        assert resp.status_code == 200
        assert resp.json == {'calls': {'test_push': 'push event'}, 'status': 'HIT'}

def test_hook_without_match(github_app):
    """Return a 200 response and valid payload for hooks with no matches"""
    with open(os.path.join(FIXURES_DIR, 'release_hook.json'), 'rb') as hook:
        issues_data = hook.read()

    github_app.config['GITHUBAPP_SECRET'] = False

    with github_app.test_client() as client:
        resp = client.post('/',
                           data=issues_data,
                           headers={
                               'Content-Type': 'application/json',
                               'X-GitHub-Event': 'release',
                           })
        assert resp.status_code == 200
        assert resp.json == {'calls': {}, 'status': 'MISS'}
