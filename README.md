# flask-githubapp [![Build Status](https://travis-ci.com/bradshjg/flask-githubapp.svg?branch=master)](https://travis-ci.com/bradshjg/flask-githubapp)
Flask extension for rapid Github app development,  in the spirit of [probot](https://probot.github.io/)

GitHub Apps help automate GitHub workflows. Examples include preventing merging of pull requests with "WIP" in the title or closing stale issues and pull requests.

## Getting Started
### Installation
To install Flask-GitHubApp:

`pip install flask-ask`

### Simple GitHub App (Cruel Closer)
We're going to develop a GitHub app that will close all opened issues with the text "Could not replicate".

#### Setup Local Environment
To make sure we can receive the GitHub hooks, install [ngrok](https://ngrok.com/) and run

`ngrok http 5000`

> We'll use the HTTPS endpoint created by ngrok as the **Webhook URL** in our Github app configuration.

#### Create GitHub App

Follow GitHub's docs on [creating a github app](https://developer.github.com/apps/building-github-apps/creating-a-github-app/).

> For this app we're going to need **Read & write** access to **Issues** and a subscription to  **Issues**
> events.

#### Build the Flask App

Create a virtualenv and install `flask-githubapp`

`python -m venv /path/to/new/venv`

`source /path/to/new/venv/bin/activate`

`pip install flask-githubapp`

Create a file named `app.py` with the following contents:

```python
import os

from flask import Flask
from flask_githubapp import GitHubApp

app = Flask(__name__)

app.config['GITHUBAPP_ID'] = int(os.environ['GITHUBAPP_ID'])

with open(os.environ['GITHUBAPP_KEY_PATH'], 'rb') as key_file:
    app.config['GITHUBAPP_KEY'] = key_file.read()

app.config['GITHUBAPP_SECRET'] = os.environ['GITHUBAPP_SECRET']

github_app = GitHubApp(app)


@github_app.on('issues.opened')
def cruel_closer():
    owner = github_app.payload['repository']['owner']['login']
    repo = github_app.payload['repository']['name']
    num = github_app.payload['issue']['number']
    issue = github_app.installation_client.issue(owner, repo, num)
    issue.create_comment('Could not replicate.')
    issue.close()
```

> The environment variables that need to be set are `GITHUBAPP_ID`, `GITHUBAPP_KEY_PATH`, and `GITHUBAPP_SECRET`.

#### Run the Flask App
`export FLASK_APP=app.py`

`flask run`

#### Install the GitHub App

**Settings** > **Applications** > **Configure**

> Any repositories that you give the GitHub app access to will cruelly close all new issues, be careful.

## Usage

### `GitHubApp` Instance Attributes

`payload`: In the context of a hook request, a Python dict representing the hook payload (raises a `RuntimeError`
outside a hook context).

`installation_client`: In the context of a hook request, a [github3.py](https://github3py.readthedocs.io/en/master/)
client authenticated as the app installation (raises a `RuntimeError` outside a hook context.)

`app_client`: A [github3.py](https://github3py.readthedocs.io/en/master/) client authenticated as the app.

`installation_token`: The token used to authenticate as the app installation (useful for passing to async tasks).

## Configuration

`GITHUBAPP_ID`: GitHub app ID as an int (required). Default: None

`GITHUBAPP_KEY`: Private key used to sign access token requests as bytes or utf-8 encoded string (required). Default: None

`GITHUBAPP_SECRET`: Secret used to secure webhooks as bytes or utf-8 encoded string (required). Default: None

`GITHUBAPP_URL`: URL of GitHub instance (used for GitHub Enterprise) as a string. Default: None

`GITHUBAPP_ROUTE`: Path used for GitHub hook requests as a string. Default: '/'
