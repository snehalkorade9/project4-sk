"""This test the homepage"""
from app import transaction, auth


@auth.route('/profile', methods=['POST', 'GET'])
def test_manage_profile(client, application, logged_in_user):
    response = client.get("/profile")
    assert response.status_code == 200
    with application.app_context():
        rv = client.post('/profile', data=dict(
            about='test test test',
        ), follow_redirects=True)
        print("rv.request.path", rv.request.path)
        assert rv.status_code == 200
        assert rv.request.path == "/dashboard"
        assert b"You Successfully Updated your Profile" in rv.data
