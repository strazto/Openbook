from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort

from openbook.auth import login_required
from openbook.db import get_db

import openbook.__init__

bp = Blueprint('root', __name__)

@bp.route('/')
def index():
    # make this point to your resume
    # return render_template('blog/index.html', posts=posts)
    return render_template('other_sites/Resume/resume.html')
    # return send_from_directory('static/other_sites/Resume', 'resume.html')

@bp.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')
    # return send_static_file('static/robots.txt')

@bp.route('/favicon.ico')
def icon():
    return send_from_directory('static', 'favicon.ico')

# Next time, serve the static files using above
# Hopefully this mean you won't have to use a template

# @bp.route('/images/openbook_image.png')
# def images():
#     return send_static_file('other_sites/Resume/images/openbook_image.png')
