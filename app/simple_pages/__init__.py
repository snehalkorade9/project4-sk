import logging

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_pages = Blueprint('simple_pages', __name__,
                        template_folder='templates')


@simple_pages.route('/')
def index():
    log = logging.getLogger("myApp")
    try:
        log.info("Home Page loaded successfully")
        return render_template('index.html')
    except TemplateNotFound:
        log.info("404 on index page")
        abort(404)

@simple_pages.route('/about')
def about():
    log = logging.getLogger("myApp")
    try:
        log.info("About Page loaded successfully")
        return render_template('about.html')
    except TemplateNotFound:
        log.info("404 on index page")
        abort(404)

@simple_pages.route('/welcome')
def welcome():
    log = logging.getLogger("myApp")
    try:
        log.info("Welcome Page loaded successfully")
        return render_template('welcome.html')
    except TemplateNotFound:
        log.info("404 on index page")
        abort(404)