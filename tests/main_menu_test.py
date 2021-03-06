"""This test the homepage"""
from app import auth


def test_main_menu_without_login(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/welcome"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


@auth.route('/dashboard')
def test_access_non_admin(client, application, logged_in_non_admin_user):
    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/account")
    assert response.status_code == 200
    response = client.get("/user")
    assert response.status_code == 404
