import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for,current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Transaction
from app.transaction.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

transaction = Blueprint('transaction', __name__,
                        template_folder='templates')

@transaction.route('/transaction', methods=['GET'], defaults={"page": 1})
@transaction.route('/transaction/<int:page>', methods=['GET'])
def transaction_browse(page):
    page = page
    per_page = 1000
    pagination = Transaction.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transaction.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@transaction.route('/transaction/upload', methods=['POST', 'GET'])
@login_required
def transaction_upload():
    print("Current user", current_user, "is admin", current_user.is_admin)
    print("in transaction upload")
    if current_user.is_admin:
        form = csv_upload()
        if form.validate_on_submit():
            log = logging.getLogger("myApp")

            filename = secure_filename(form.file.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            #user = current_user
            list_of_transaction = []
            with open(filepath) as file:
                csv_file = csv.DictReader(file)
                for row in csv_file:
                    list_of_transaction.append(Transaction(row['AMOUNT'], row['Type']))

            current_user.transaction = list_of_transaction
            db.session.commit()

            return redirect(url_for('transaction.transaction_browse'))
        try:
            return render_template('upload.html', form=form)
        except TemplateNotFound:
            abort(404)
    else:
        return redirect(url_for('transaction.transaction_browse'), 403)