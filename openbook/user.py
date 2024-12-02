import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from openbook.auth import login_required
from openbook.db import get_db

bp = Blueprint('user', __name__, url_prefix='/blog/user')

@bp.route('/admin')
@login_required
def admin():

    db = get_db()
    users = db.execute(
        'SELECT * from user;'
    ).fetchall()
    
    return render_template('user/admin.html', users=users)

@bp.route('/me')
@login_required
def me():

    return render_template('user/me.html')

