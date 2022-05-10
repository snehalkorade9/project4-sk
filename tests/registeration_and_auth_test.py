from app import auth


@auth.route('/register', methods=['POST', 'GET'])
def test_register_user(client, application):
    response = client.get("/register")
    assert response.status_code == 200
    with application.app_context():
        rv = client.post('/register', data=dict(
            email='sk2@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        print("rv.request.path", rv.request.path)
        assert rv.status_code == 200
        assert rv.request.path == "/login"
        assert b"Congratulations" in rv.data


@auth.route('/login', methods=['POST', 'GET'])
def test_user_login(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#',
            #testing password
        ), follow_redirects=True)
        assert rv.request.path == "/dashboard"
        assert b"Welcome1" in rv.data
