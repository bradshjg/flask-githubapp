import os

from flask import Flask
from flask_githubapp import GitHubApp

app = Flask(__name__)

app.config['GITHUBAPP_ID'] = os.environ['GITHUBAPP_ID']

with open(os.environ['GITHUBAPP_KEY_PATH'], 'rb') as key_file:
    app.config['GITHUBAPP_KEY'] = key_file.read()

github_app = GitHubApp(app)


@github_app.on('issues.opened')
def cruel_closer(context):
    owner = context.payload['repository']['owner']['login']
    repo = context.payload['repository']['name']
    num = context.payload['issue']['number']
    issue = context.github.issue(owner, repo, num)
    issue.create_comment('Could not replicate.')
    issue.close()
