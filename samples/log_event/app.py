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
