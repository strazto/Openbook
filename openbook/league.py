import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from openbook.auth import login_required
from openbook.db import get_db

bp = Blueprint('league', __name__, url_prefix='/blog')

@bp.route('/league')
@login_required
def league():
    
    return render_template('league/league.html')

