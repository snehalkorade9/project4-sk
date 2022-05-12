import logging

from app import db, User
from app.db.models import Transaction


def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        #showing how to add a record
        #create a record
        user = User('ske@test.com', 'test1254')
        #add it to get ready to be committed
        db.session.add(user)
        user = User.query.filter_by(email='ske@test.com').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'ske@test.com'
        #this is how you get a related record ready for insert
