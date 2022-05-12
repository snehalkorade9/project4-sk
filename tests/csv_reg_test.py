from app import auth



@auth.route('/register', methods=['POST', 'GET'])
def test_invalid_register_user_valid_same(client, application, create_user):
    response = client.get("/register")
    assert response.status_code == 200
    with application.app_context():
        rv = client.post('/register', data=dict(
            email='sk@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        print("rv.request.path", rv.request.path)
        assert rv.status_code == 200
        assert rv.request.path == "/login"
        assert b"Already" in rv.data



@auth.route('/login', methods=['POST', 'GET'])
def test_user_login_test(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#',
            #testing password
        ), follow_redirects=True)
        assert rv.request.path == "/dashboard"
        assert b"Welcome1" in rv.data


@auth.route('/login', methods=['POST', 'GET'])
def test_invalid_login_test(client, application, create_user):
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


@auth.route('/dashboard')
def test_dashboard_access_denyed(client, application):
    with application.app_context():
        #user = User.query.get(User.id)test
        response = client.get("/dashboard")
        assert response.status_code == 302
