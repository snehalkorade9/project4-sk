from app import auth


@auth.route('/users', methods=['POST'])
def test_edit_user_fun(client, application, logged_in_user):
    response = client.get("users/1/edit")
    with application.app_context():
        rv = client.post('users/1/edit', data=dict(
            about='sk1@njit.edu' ), follow_redirects=True)
        assert b'User Edited Successfully' in rv.data


