"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import logging
import os

import pytest
from werkzeug.security import generate_password_hash

from app import create_app, User
from app.db import db

@pytest.fixture()
def application():
    """This makes the app"""
    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()



@pytest.fixture()
def create_user(application):
        with application.app_context():
            # new record
            user = User('sk@njit.edu', generate_password_hash('Test123#'))
            user.is_admin = 1
            db.session.add(user)
            db.session.commit()
            user = User('sk1@njit.edu', generate_password_hash('Test123#'))
            db.session.add(user)
            db.session.commit()

@pytest.fixture()
def logged_in_user(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#'     #testing password
        ), follow_redirects=True)


@pytest.fixture()
def logged_in_non_admin_user(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk1@njit.edu',
            password='Test123#'     #testing password
        ), follow_redirects=True)