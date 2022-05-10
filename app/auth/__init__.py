import logging

from flask import Blueprint, render_template, redirect, url_for, flash,current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form, create_user_form
from app.db import db
from app.db.models import User, Transaction

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    log = logging.getLogger("myApp")
    if current_user.is_authenticated:
        print("Current user",current_user)
        return redirect(url_for('auth.dashboard'))
    form = register_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        log.info(user)
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()
            flash('Congratulations, you are now a registered user!', "success")
            log.info("Registered successfully")
            return redirect(url_for('auth.login'), 302)
        else:
            flash('Already Registered')
            log.info("User Already Registered")
            return redirect(url_for('auth.login'), 302)
    return render_template('register.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    log = logging.getLogger("myApp")
    form = login_form()
    if current_user.is_authenticated:
        log.info("valid user")
        return redirect(url_for('auth.dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        log.info(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            log.info("Invalid username or password")
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            log.info("User logged in")
            flash("Welcome1", 'success')
            return redirect(url_for('auth.dashboard'))
    return render_template('login.html', form=form)

@auth.route("/logout")
@login_required
def logout():
    log = logging.getLogger("myApp")
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    log.info(user)
    log.info("Logout")
    return redirect(url_for('auth.login'))



@auth.route('/dashboard')
@login_required
def dashboard():
    log = logging.getLogger("myApp")
    data = Transaction.query.filter_by(user_id=current_user.id)
    #print("data", data, "datatype")
    if current_user.is_authenticated:
        return render_template('dashboard.html')
        #return render_template('dashboard.html', data=data)
    else:
        log.info("unauthorized user")
        return redirect(url_for('auth.dashboard'), 403)

@auth.route('/profile', methods=['POST', 'GET'])
def edit_profile():
    log = logging.getLogger("myApp")
    user = User.query.get(current_user.get_id())
    form = profile_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Profile', 'success')
        log.info("user profile updated with about")
        log.info(user.about)
        return redirect(url_for('auth.dashboard'))
    return render_template('profile_edit.html', form=form)


@auth.route('/account', methods=['POST', 'GET'])
def edit_account():
    log = logging.getLogger("myApp")
    user = User.query.get(current_user.get_id())
    form = security_form(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('You Successfully Updated your Password or Email', 'success')
        log.info("Updated your Password or Email")
        return redirect(url_for('auth.dashboard'))
    return render_template('manage_account.html', form=form)



#You should probably move these to a new Blueprint to clean this up.  These functions below are for user management

@auth.route('/users')
@login_required
@admin_required
def browse_users():
    data = User.query.all()
    log = logging.getLogger("myApp")
    titles = [('email', 'Email'), ('registered_on', 'Registered On')]
    retrieve_url = ('auth.retrieve_user', [('user_id', ':id')])
    edit_url = ('auth.edit_user', [('user_id', ':id')])
    add_url = url_for('auth.add_user')
    delete_url = ('auth.delete_user', [('user_id', ':id')])
    log.info("Browse User")
    current_app.logger.info("Browse page loading")

    return render_template('browse.html', titles=titles, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           retrieve_url=retrieve_url, data=data, User=User, record_type="Users")


@auth.route('/users/<int:user_id>')
@login_required
def retrieve_user(user_id):
    log = logging.getLogger("myApp")
    user = User.query.get(user_id)
    log.info(user)
    log.info("User details")
    return render_template('profile_view.html', user=user)


@auth.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    log = logging.getLogger("myApp")
    user = User.query.get(user_id)
    form = user_edit_form(obj=user)
    if form.validate_on_submit():
        user.about = form.about.data
        log.info(user.about)
        user.is_admin = int(form.is_admin.data)
        log.info(user.is_admin)
        db.session.add(user)
        db.session.commit()
        user.is_admin("User Edited Successfully")
        flash('User Edited Successfully', 'success')
        current_app.logger.info("edited a user")
        return redirect(url_for('auth.browse_users'))
    return render_template('user_edit.html', form=form)


@auth.route('/users/new', methods=['POST', 'GET'])
@login_required
def add_user():
    form = create_user_form()
    log = logging.getLogger("myApp")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        log.info(user)
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data))#, is_admin = int(form.is_admin.data))
            db.session.add(user)
            log.user('created a user')
            db.session.commit()
            flash('Congratulations, you just created a user', 'success')
            return redirect(url_for('auth.browse_users'))
        else:
            flash('Already Registered')
            log.info('user Already Registered')
            return redirect(url_for('auth.browse_users'))
    return render_template('user_new.html', form=form)

@auth.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    log = logging.getLogger("myApp")
    user = User.query.get(user_id)
    log.info(user)
    if user.id == current_user.id:
        flash("You can't delete yourself!")
        log.info("can't delete yourself")
        return redirect(url_for('auth.browse_users'), 302)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted', 'success')
    log.info("User deleted")
    return redirect(url_for('auth.browse_users'), 302)






