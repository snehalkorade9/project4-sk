from app import auth


@auth.route('/account', methods=['POST', 'GET'])
def test_valid_user_login(client, application, logged_in_user):
    with application.app_context():
        rv = client.post('/account', data=dict(
            email='sk2@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        assert rv.status_code == 200
