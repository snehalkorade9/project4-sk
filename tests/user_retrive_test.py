from app import auth


@auth.route('/users/1', methods=['POST'])
def test_edit_user_fun(client, application, logged_in_user):
    response = client.get("users/1")
    assert b'User Email: sk@njit.edu' in response.data

