import io

from app import transaction


@transaction.route('/transactions/upload')
def test_upload_file(client, application, logged_in_user):
    with application.app_context():
        response = client.get("/transaction/upload")
        assert response.status_code == 200
        #filepath/home/myuser/app/uploads/transactions_2.csv
        csv = b"D:/Project4/app/uploads/transactions_2.csv"
        csv_read=(io.BytesIO(csv))
        csv_data = open(csv, "rb")
        data = {"file": (csv_data, "transactions 2")}

        rv=client.post(
            data=data,
            buffered=True,
        )
        assert rv.status_code == 200

