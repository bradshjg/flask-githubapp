from flask_githubapp.core import GitHubApp, GitHubAppEventHandler

__all__ = ["GitHubApp", "GitHubAppEventHandler"]

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

# Set initial level to WARN. Users must manually enable logging for
# flask_githubapp to see our logging.
rootlogger = logging.getLogger(__name__)
rootlogger.addHandler(NullHandler())

if rootlogger.level == logging.NOTSET:
    rootlogger.setLevel(logging.WARNING)
