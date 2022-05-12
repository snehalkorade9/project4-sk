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
def test_links_post_login_invalid(client, application, logged_in_user):
    with application.app_context():
        #user = User.query.get(User.id)
        response = client.get("/dashboard")
        assert response.status_code == 200
        response = client.get("/profile")
        assert response.status_code == 200
        response = client.get("/account")
        assert response.status_code == 200
        response = client.get("/users")
        assert response.status_code == 200
        response = client.get("/transaction")
        assert response.status_code == 200
        response = client.get("/about")
        assert response.status_code == 200
        response = client.get("/welcome")
        assert response.status_code == 200