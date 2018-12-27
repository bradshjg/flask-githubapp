import os

from flask import Flask
from flask_githubapp import GitHubApp

app = Flask(__name__)

app.config['GITHUBAPP_ID'] = int(os.environ['GITHUBAPP_ID'])

with open(os.environ['GITHUBAPP_KEY_PATH'], 'rb') as key_file:
    app.config['GITHUBAPP_KEY'] = key_file.read()

app.config['GITHUBAPP_SECRET'] = os.environ['GITHUBAPP_SECRET'].encode('utf-8')

github_app = GitHubApp(app)


@github_app.on('issues.opened')
def cruel_closer():
    owner = github_app.payload['repository']['owner']['login']
    repo = github_app.payload['repository']['name']
    num = github_app.payload['issue']['number']
    issue = github_app.installation_client.issue(owner, repo, num)
    issue.create_comment('Could not replicate.')
    issue.close()
