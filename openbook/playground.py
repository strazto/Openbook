import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)

from openbook.auth import login_required
from openbook.db import get_db

bp = Blueprint('playground', __name__, url_prefix='/blog/playground')

@bp.route('/three')
def three():   
    return render_template('playground/three.html')

@bp.route('/index.js')
def index():
	return send_from_directory('static', 'index.js')

@bp.route('/index2.js')
def index2():
	return send_from_directory('static', 'index2.js')

@bp.route('/index3.js')
def index3():
	return send_from_directory('static', 'index3.js')

	# I do not understand why this can only be done via the static folder
	# Perhaps a setting

	# https://runebook.dev/en/articles/flask/api/index/flask.send_from_directory

	# return send_from_directory('templates/playgound', 'three.html')
	# return url_for('static', filename='index.js')
