import os
from typing import io

from flask import current_app
from werkzeug.utils import secure_filename

from app import transaction, auth


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


def test_log_folder_creation():
    """check if info.log is created"""
    root = os.path.dirname(os.path.abspath(__file__))
    print (os.path.join(root, "/Project4/app/uploads"))
    assert os.path.exists(os.path.join(root, "../app/uploads")) == True



