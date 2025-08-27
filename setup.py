"""
Flask-GitHubApp
---------------

Easy GitHub App integration for Flask
"""
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'src/flask_githubapp/version.py'), 'r') as f:
    exec(f.read())


setup(
    name='Flask-GitHubApp',
    package_dir = {"": "src"},
    version=__version__,
    url='https://github.com/bradshjg/flask-githubapp',
    license='MIT',
    author='Jimmy Bradshaw',
    author_email='james.g.bradshaw@gmail.com',
    description='Rapid GitHub app development in Python',
    long_description=__doc__,
    packages=['flask_githubapp'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'flask',
        'github3.py'
    ],
)
