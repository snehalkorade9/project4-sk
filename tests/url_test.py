"""This test the homepage"""
import os


def test_url(client):
    """This makes the index page"""
    response = client.get("/")
    print(os.getcwd())
    assert response.status_code == 200

