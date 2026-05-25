# flask-githubapp

Flask extension for rapid Github app development in Python, in the spirit of [probot](https://probot.github.io/)

## Getting Started

### Installation

`pip install flask-githubapp`

> [!NOTE]
> `flask-githubapp` requires a supported Python version and Flask 2+

#### Create a GitHub App

Follow GitHub's docs on [creating a github app](https://developer.github.com/apps/building-github-apps/creating-a-github-app/).

#### Build the Flask App

The following example shows both styles of exposing event handlers, the functional and class style.

[`samples/log_event/app.py`](./samples/log_event/app.py)

```python
import base64
import logging
import os

from flask import Flask

from flask_githubapp import GitHubApp, GitHubAppEventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["GITHUBAPP_ID"] = os.environ["GITHUBAPP_ID"]
    app.config["GITHUBAPP_KEY"] = base64.b64decode(os.environ["GITHUBAPP_KEY_B64"])
    app.config["GITHUBAPP_SECRET"] = os.environ["GITHUBAPP_SECRET"]

    if test_config:
        app.config.update(test_config)

    github_app = GitHubApp(app)

    @github_app.on("issue_comment.created")
    def log_issue_comment():
        comment_body = github_app.payload["comment"]["body"]
        logger.info(comment_body)

    LogIssue(github_app=github_app)

    return app


class LogIssue(GitHubAppEventHandler):
    logger = logging.getLogger(__name__)

    @property
    def events(self):
        return ["issues.opened"]

    def call(self):
        issue_body = self.payload["issue"]["body"]
        self.logger.info(issue_body)

```

```python
@github_app.on("issue_comment.created")
def log_issue_comment():
    ...

class LogIssue(GitHubAppEventHandler):
    @property
    def events(self):
        return ["issues.opened"]
...
```

Are how handlers register themselves for events. The syntax is `<event>[.<action>]` where the event comes from the
`X-GitHub-Event` header and the action from the payload. The action is optional.

#### Run it locally

For local development, [smee.io](https://smee.io) is the recommended proxy. If you'd like to disable webhook validation,
you can supply `app.config["GITHUBAPP_SECRET"] = False`.

```bash
EXPORT GITHUBAPP_SECRET=False # this will circumvent request verification
EXPORT FLASK_APP=/path/to/your/flask/app.py # the file does not need to be named app.py! But it has to be the python file that instantiates the Flask app. For instance, samples/cruel_closer/app.py
```

#### Testing

See [`samples/log_event`](./samples/log_event/) which inclues pytest configuration and some simple tests.

## Usage

### `GitHubApp` Instance Attributes

`payload`: In the context of a hook request, a Python dict representing the hook payload (raises a `RuntimeError`
outside a hook context).

`installation_client`: In the context of a hook request, a [github3.py](https://github3py.readthedocs.io/en/master/) client authenticated as the app installation (raises a `RuntimeError` outside a hook context.)

`app_client`: A [github3.py](https://github3py.readthedocs.io/en/master/) client authenticated as the app.

`installation_token`: The token used to authenticate as the app installation (useful for passing to async tasks).

> [!NOTE]
> These same attributes are also available as method to handlers that inherit `GitHubAppEventHandler`

## Configuration

`GITHUBAPP_ID`: GitHub app ID as an int (required). Default: None

`GITHUBAPP_KEY`: Private key used to sign access token requests as bytes or utf-8 encoded string (required). Default: None

`GITHUBAPP_SECRET`: Secret used to secure webhooks as bytes or utf-8 encoded string (required). Set to `False` to disable
verification.

`GITHUBAPP_URL`: URL of GitHub instance (used for GitHub Enterprise) as a string. Default: None

`GITHUBAPP_ROUTE`: Path used for GitHub hook requests as a string. Default: '/'
