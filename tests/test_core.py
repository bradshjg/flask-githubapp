import json
from unittest.mock import MagicMock

from github3 import GitHub, GitHubEnterprise

from flask_githubapp import GitHubApp
from flask_githubapp.core import STATUS_NO_FUNC_CALLED


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
    assert 'GITHUBAPP_URL' not in app.config


def test_github_client(app):
    github_app = GitHubApp(app)
    with app.app_context():
        assert isinstance(github_app.client, GitHub)


def test_github_enterprise_client(app):
    enterprise_url = 'https://enterprise.github.com'
    app.config['GITHUBAPP_URL'] = enterprise_url
    github_app = GitHubApp(app)
    with app.app_context():
        assert isinstance(github_app.client, GitHubEnterprise)
        assert github_app.client.url == enterprise_url


def test_github_installation_client(app, mocker):
    github_app = GitHubApp(app)
    installation_id = 2
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    mock_client = mocker.patch('flask_githubapp.core.GitHubApp.client')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': installation_id}}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        github_app.installation_client
        mock_client.login_as_app_installation.assert_called_once_with(github_app.key,
                                                                      github_app.id,
                                                                      installation_id)


def test_github_installation_client_is_lazy(app, mocker):
    github_app = GitHubApp(app)
    installation_id = 2
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    mock_client = mocker.patch('flask_githubapp.core.GitHubApp.client')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': installation_id}}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        mock_client.login_as_app_installation.assert_not_called()


def test_github_app_client(app, mocker):
    github_app = GitHubApp(app)
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    mock_client = mocker.patch('flask_githubapp.core.GitHubApp.client')
    with app.app_context():
        github_app.app_client
        mock_client.login_as_app.assert_called_once_with(github_app.key,
                                                         github_app.id)


def test_hook_mapping(app):
    github_app = GitHubApp(app)

    @github_app.on('foo')
    def bar():
        pass

    assert github_app._hook_mappings['foo'] == [bar]


def test_multiple_function_on_same_event(app):
    github_app = GitHubApp(app)

    @github_app.on('foo')
    def bar():
        pass

    @github_app.on('foo')
    def baz():
        pass

    assert github_app._hook_mappings['foo'] == [bar, baz]


def test_events_mapped_to_functions(app, mocker):
    github_app = GitHubApp(app)

    function_to_call = MagicMock()
    function_to_call.__name__ = 'foo'  # used to generate response
    function_to_call.return_value = 'foo'  # return data must be serializable

    github_app._hook_mappings['foo'] = [function_to_call]
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2}}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        function_to_call.assert_called_once_with()


def test_events_with_actions_mapped_to_functions(app, mocker):
    github_app = GitHubApp(app)

    function_to_call = MagicMock()
    function_to_call.__name__ = 'foo'  # used to generate response
    function_to_call.return_value = 'foo'  # return data must be serializable

    github_app._hook_mappings['foo.bar'] = [function_to_call]
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2},
                                            'action': 'bar'}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        function_to_call.assert_called_once_with()


def test_functions_can_return_no_data(app, mocker):
    github_app = GitHubApp(app)

    function_to_call = MagicMock()
    function_to_call.__name__ = 'foo'  # used to generate response
    function_to_call.return_value = None

    github_app._hook_mappings['foo'] = [function_to_call]
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2}}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        function_to_call.assert_called_once_with()


def test_function_exception_raise_500_error(app, mocker):
    github_app = GitHubApp(app)

    function_to_call = MagicMock()
    function_to_call.__name__ = 'foo'  # used to generate response
    function_to_call.side_effect = Exception('foo exception')

    github_app._hook_mappings['foo'] = [function_to_call]
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2}}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 500
        function_to_call.assert_called_once_with()


def test_no_target_functions(app, mocker):
    github_app = GitHubApp(app)

    function_to_miss = MagicMock()
    function_to_miss.__name__ = 'foo'  # used to generate response

    github_app._hook_mappings['foo'] = [function_to_miss]
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2}}),
                           headers={
                              'X-GitHub-Event': 'bar',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        function_to_miss.assert_not_called()
        assert resp.json['status'] == STATUS_NO_FUNC_CALLED
        assert resp.json['calls'] == {}


def test_view_returns_map_of_called_functions_and_returned_data(app, mocker):
    github_app = GitHubApp(app)

    def event_function():
        return 'foo'

    def event_action_function():
        return 'bar'

    def other_event_function():
        return 'baz'

    github_app._hook_mappings = {
        'foo': [event_function],
        'foo.bar': [event_action_function],
        'bar': [other_event_function]
    }
    mocker.patch('flask_githubapp.core.GitHubApp._verify_webhook')
    with app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2},
                                            'action': 'bar'}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 200
        assert resp.json == {
            'status': 'HIT',
            'calls': {
                'event_function': 'foo',
                'event_action_function': 'bar',
            }
        }

def test_invalid_json_header_returns_error(github_app):
    """HTTP request have a valid json content type"""
    github_app.config['GITHUBAPP_SECRET'] = False
    with github_app.test_client() as client:
        resp = client.post('/',
                           data=json.dumps({'installation': {'id': 2},
                                            'action': 'bar'}),
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'text/plain'
                           })
        assert resp.status_code == 400
        assert resp.json == {
            'status': 'ERROR',
            'description': 'Invalid HTTP Content-Type header for JSON body '
                           '(must be application/json or application/*+json).'
        }

def test_invalid_json_body_returns_error(github_app):
    """HTTP request have a valid json body"""
    github_app.config['GITHUBAPP_SECRET'] = False
    with github_app.test_client() as client:
        resp = client.post('/',
                           data='invalid json',
                           headers={
                              'X-GitHub-Event': 'foo',
                              'Content-Type': 'application/json'
                           })
        assert resp.status_code == 400
        assert resp.json == {
            'status': 'ERROR',
            'description': 'Invalid HTTP body (must be JSON).'
        }
