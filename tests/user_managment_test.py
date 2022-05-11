"""This test the homepage"""
from app import transaction, auth


@auth.route('/users', methods=['POST', 'GET'])
def test_user_display(client, application, logged_in_user):
    response = client.get("/users")
    assert b"sk@njit.edu" in response.data



