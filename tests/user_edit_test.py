"""This test the homepage"""
from flask import url_for

from app import auth


@auth.route('/users', methods=['POST', 'GET'])
def test_user_display(client, application, logged_in_user):
    response = client.get("/users")
    assert b"sk@njit.edu" in response.data




@auth.route('/users/new', methods=['POST', 'GET'])
def test_new_user_creation(client, application, logged_in_user):
    response = client.get("/users/new")
    assert response.status_code == 200
    with application.app_context():
        rv = client.post('/users/new', data=dict(
            email='sk8@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert b'Congratulations, you just created a u' in rv.data


@auth.route('/users/new', methods=['POST', 'GET'])
def test_new_user_exist(client, application, logged_in_user):
    response = client.get("/users/new")
    assert response.status_code == 200
    with application.app_context():
        rv = client.post('/users/new', data=dict(
            email='sk@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert b'Already Registered' in rv.data



@auth.route('/users', methods=['POST'])
def test_delete_existing_user(client, application, logged_in_user):
    response = client.get("users/1/delete")
    with application.app_context():
        rv = client.post('users/1/delete', data=dict(
            email='sk@njit.edu' ), follow_redirects=True)
        assert rv.status_code == 200
        assert b'delete yourself!' in rv.data

