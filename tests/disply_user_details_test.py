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
def test_invalid_user_login(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk123@njit.edu',
            password='testtest'
        ), follow_redirects=True)
        assert b"Invalid username or password" in rv.data
        rv = client.post('/login', data=dict(
            email='s1234@njit.com',
            password='Test123#'
        ), follow_redirects=True)
        assert b"Invalid username or password" in rv.data



@auth.route('/transaction')
def test_dashboard_access_denyed_for_unauthorized_user(client, application):
    with application.app_context():
        #user = User.query.get(User.id)test
        response = client.get("/dashboard")
        assert response.status_code == 302




