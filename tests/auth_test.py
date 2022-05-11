from app import transaction

@transaction.route('/transactions/upload')
def test_allow_upload_file(client, application, logged_in_user):
    with application.app_context():
        response = client.get("/transaction/upload")
        #print("loggen in", response.data)
        assert response.status_code == 200


@transaction.route('/transactions/upload')
def test_deney_access_upload_file(client, application, logged_in_non_admin_user):
    with application.app_context():
        response = client.get("/transaction/upload")
        #print("loggen in", response.data)
        assert response.status_code == 403