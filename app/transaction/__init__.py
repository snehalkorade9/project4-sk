import csv
import logging
import os
from sqlalchemy import insert
from flask import Blueprint, render_template, abort, url_for,current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Transaction, User
from app.transaction.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

transaction = Blueprint('transaction', __name__,
                        template_folder='templates')

@transaction.route('/transaction', methods=['GET'], defaults={"page": 1})
@transaction.route('/transaction/<int:page>', methods=['GET'])
def transaction_browse(page):
    log = logging.getLogger("myApp")
    page = page
    per_page = 1000
    sum = 0
    total = 0
    pagination = Transaction.query.paginate(page, per_page, error_out=False)
    log.info("Display transactions")
    data = pagination.items
    for transaction in data:
        total = total + transaction.amount
        transaction.balance = total
        db.session.commit()
        print(total)
        if transaction.user_id == current_user.id:
            sum = sum + transaction.amount
    current_user.sum = sum

    log.info("Sum of user's")
    #log.info(current_user.id)
    log.info("transactions")
    log.info(sum)
    db.session.commit()
    try:
        #db.session.commit()
        return render_template('browse_transaction.html', data=data, pagination=pagination)
    except TemplateNotFound:
        log.info("Display transaction Page not found")
        abort(404)

@transaction.route('/transaction/upload', methods=['POST', 'GET'])
@login_required
def transaction_upload():
    log = logging.getLogger("myApp")
    if current_user.is_admin:
        form = csv_upload()
        if form.validate_on_submit():
            log = logging.getLogger("myApp")
            filename = secure_filename(form.file.data.filename)
            print(filename)
            log.info("Upload file from")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            log.info(filepath)
            form.file.data.save(filepath)
            #user = current_user.
            list_of_transaction = []
            with open(filepath, newline='') as file:
                csv_file = csv.DictReader(file)
                for row in csv_file:
                    list_of_transaction.append(Transaction(row['AMOUNT'], row['TYPE']))
            current_user.transaction = list_of_transaction
            log.info("file uploaded successfully")
            db.session.commit()
            return redirect(url_for('transaction.transaction_browse'))
        try:
            return render_template('upload.html', form=form)
        except TemplateNotFound:
            log.info("Upload transaction Page not found")
            abort(404)
    else:
        log.info("Unauthorized")
        return redirect(url_for('transaction.transaction_browse'), 403)