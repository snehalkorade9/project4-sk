from app import auth


@auth.route('/account', methods=['POST', 'GET'])
def test_valid_user_login(client, application, logged_in_user):
    with application.app_context():
        rv = client.post('/account', data=dict(
            email='sk2@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        print("rv.request.path", rv.request.path)
        assert rv.status_code == 200


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
        print("rv.request.path", rv.request.path)
        assert rv.status_code == 200
        assert b'Congratulations, you just created a u' in rv.data


