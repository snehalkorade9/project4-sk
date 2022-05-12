from app import transaction


@transaction.route('/transactions/upload')
def test_upload_file(client, application, logged_in_user):
    with application.app_context():
        response = client.get("/transaction/upload")
        assert response.status_code == 200