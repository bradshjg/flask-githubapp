# flask-githubapp [![Build Status](https://travis-ci.com/bradshjg/flask-githubapp.svg?branch=master)](https://travis-ci.com/bradshjg/flask-githubapp)
Flask extension for rapid Github app development in Python, in the spirit of [probot](https://probot.github.io/)

GitHub Apps help automate GitHub workflows. Examples include preventing merging of pull requests with "WIP" in the title or closing stale issues and pull requests.

## Getting Started

### Installation
To install Flask-GitHubApp:

`pip install flask-githubapp`

Or better yet, add it to your app's requirements.txt file! ;)

#### Create GitHub App

Follow GitHub's docs on [creating a github app](https://developer.github.com/apps/building-github-apps/creating-a-github-app/).

> You can, in principle, register any type of payload to be sent to the app!

Once you do this, please note down the GitHub app Id, the GitHub app secret, and make sure to [create a private key](https://docs.github.com/en/developers/apps/authenticating-with-github-apps#generating-a-private-key) for it! These three elements are __required__ to run your app.

#### Build the Flask App

The GithubApp package has a decorator, `@on`, that will allow you to register events, and actions, to specific functions.
For instance,

```python
@github_app.on('issues.opened')
def cruel_closer():
    #do stuff here
```

Will trigger whenever the app receives a Github payload with the `X-Github-Event` header set to `issues`, and an `action` field in the payload field containing `opened`
Following this logic, you can make your app react in a unique way for every combination of event and action. Refer to the Github documentation for all the details about events and the actions they support, as well as for sample payloads for each.
You can also have something like

```python
@github_app.on('issues')
def issue_tracker():
    #do stuff here
```

The above function will do `stuff here` for _every_ `issues` event received. This can be useful for specific workflows, to bring developers in early.

Inside the function, you can access the received request via the conveniently named `request` variable. You can access its payload by simply getting it: `request.payload`

You can find a complete example (containing this cruel_closer function), in the samples folder of this repo. It is a fully functioning flask Github App. Try to guess what it does!

#### Run it locally

For quick iteration, you can set up your environment as follows:

```bash
EXPORT GITHUBAPP_SECRET=False # this will circumvent request verification
EXPORT FLASK_APP=/path/to/your/flask/app.py # the file does not need to be named app.py! But it has to be the python file that instantiates the Flask app. For instance, samples/cruel_closer/app.py
```

This will make your flask application run in debug mode. This means that, as you try sending payloads and tweak functions, fix issues, etc., as soon as you save the python code, the flask application will reload itself and run the new code immediately.
Once that is in place, run your github app

```bash
flask run
```

Now, you can send requests! The port is 5000 by default but that can also be overridden. Check `flask run --help` for more details. Anyway! Now, on to sending test payloads!

```bash
curl -H "X-GitHub-Event: <your_event>" -H "Content-Type: application/json" -X POST -d @./path/to/payload.json http://localhost:5000
```

#### Install your GitHub App

**Settings** > **Applications** > **Configure**

> If you were to install the cruel closer app, any repositories that you give the GitHub app access to will cruelly close all new issues, be careful.

#### Deploy your GitHub App

Bear in mind that you will need to run the app _somewhere_. It is possible, and fairly easy, to host the app in something like Kubernetes, or simply containerised, in a machine somewhere. You will need to be careful to expose the flask app port to the outside world so the app can receive the payloads from Github. The deployed flask app will need to be reachable from the same URL you set as the `webhook url`. However, this is getting a little bit into Docker/Kubernetes territory so we will not go too deep.

## Usage

### `GitHubApp` Instance Attributes

`payload`: In the context of a hook request, a Python dict representing the hook payload (raises a `RuntimeError`
outside a hook context).

`installation_client`: In the context of a hook request, a [github3.py](https://github3py.readthedocs.io/en/master/) client authenticated as the app installation (raises a `RuntimeError` outside a hook context.)

`app_client`: A [github3.py](https://github3py.readthedocs.io/en/master/) client authenticated as the app.

`installation_token`: The token used to authenticate as the app installation (useful for passing to async tasks).

## Configuration

`GITHUBAPP_ID`: GitHub app ID as an int (required). Default: None

`GITHUBAPP_KEY`: Private key used to sign access token requests as bytes or utf-8 encoded string (required). Default: None

`GITHUBAPP_SECRET`: Secret used to secure webhooks as bytes or utf-8 encoded string (required). Set to `False` to disable
verification.

`GITHUBAPP_URL`: URL of GitHub instance (used for GitHub Enterprise) as a string. Default: None

`GITHUBAPP_ROUTE`: Path used for GitHub hook requests as a string. Default: '/'

You can find an example on how to init all these config variables in the [cruel_closer sample app](https://github.com/bradshjg/flask-githubapp/tree/master/samples/cruel_closer)

#### Cruel Closer

The cruel_closer sample app will use information of the received payload (which is received every time an issue is opened), will _find_ said issue and **close it** without regard. 
That's just r00d!