"""Flask extension for rapid GitHub app development"""
from flask import current_app, request
from github3 import GitHub, GitHubEnterprise


GITHUB_API_URL = 'https://api.github.com'


class Context:
    """GitHub hook context passed to functions

    Arguments:
        payload {dict} -- GitHub hook payload
    """

    def __init__(self, payload):
        self.payload = payload
        self._client_class = GitHub if current_app.github_app.api_url == GITHUB_API_URL else GitHubEnterprise
        client = self._client_class()
        client.login_as_app_installation(current_app.github_app.key,
                                         current_app.github_app.id,
                                         payload['installation']['id'])
        self.github = client
        self.token = client.session.auth.token


class GitHubApp(object):
    """The GitHubApp object provides the central interface for interacting GitHub hooks.

    GitHubApp object maps GitHub hooks to functions and provides a context object with an
    authenticated github3.py session. The constructor is passed a Flask App instance.
    The GitHubApp instance provides a simple decorator to route GitHub hooks to functions.

    Keyword Arguments:
        app {Flask object} -- App instance - created with Flask(__name__) (default: {None})
        route {string} -- Flask view route (default: {'/'})
    """

    def __init__(self, app=None, route='/'):
        self.app = app
        self._route = route
        self._hook_mappings = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes GitHubApp app by setting configuration variables.

        The GitHubApp instance is given the following configuration variables by calling on Flask's configuration:

        `GITHUBAPP_ID`:

            GitHub app ID as an int.
            Default: None

        `GITHUBAPP_KEY`:

            Private key used to sign access token requests as bytes.
            Default: None

        `GITHUBAPP_API_URL`:

            URL of GitHub API (used for GitHub Enterprise) as a string.
            Default: 'https://api.github.com'
        """
        self.app = app

        app.github_app = self

        app.add_url_rule(self._route, view_func=self._flask_view_func, methods=['POST'])

    @property
    def id(self):
        return current_app.config.get('GITHUBAPP_ID')

    @property
    def key(self):
        return current_app.config.get('GITHUBAPP_KEY')

    @property
    def api_url(self):
        return current_app.config.get('GITHUBAPP_API_URL', GITHUB_API_URL)

    def on(self, event_action):
        """Decorator routes a GitHub hook to the wrapped function.

        Functions decorated as a hook recipient are registered as the function for the given GitHub event.

        @github_app.on('issues.opened')
        def cruel_closer(context):
            owner = context.payload['repository']['owner']['login']
            repo = context.payload['repository']['name']
            num = context.payload['issue']['id']
            issue = context.github.issue(owner, repo, num)
            issue.create_comment('Could not replicate.')
            issue.close()

        Arguments:
            event_action {str} -- Name of the event and optional action (separated by a period), e.g. 'issues.opened' or
                'pull_request'
        """
        def decorator(f):
            self._hook_mappings[event_action] = f

            # make sure the function can still be called normally (e.g. if a user wants to pass in their
            # own Context for whatever reason).
            return f

        return decorator

    def _flask_view_func(self):
        functions_to_call = []
        event = request.headers['X-GitHub-Event']
        action = request.json.get('action')

        if event in self._hook_mappings:
            functions_to_call.append(self._hook_mappings[event])

        event_action = '.'.join([event, action])
        if event_action in self._hook_mappings:
            functions_to_call.append(self._hook_mappings[event_action])

        if functions_to_call:
            context = Context(request.json)
            for function in functions_to_call:
                function(context)
        return "OK", 200
