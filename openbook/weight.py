from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from openbook.auth import login_required
from openbook.db import get_db

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

bp = Blueprint('weight', __name__)

@login_required
@bp.route('/weight', methods=('GET', 'POST'))
def index():

	db = get_db()

	weights = db.execute(f'SELECT w.id, weight, comment, created, author_id, username FROM weight w JOIN user u ON w.author_id = u.id WHERE u.id is "{g.user['id']}" ORDER BY created DESC').fetchall()

	graph_time = db.execute(f'SELECT created FROM weight w JOIN user u on w.author_id = u.id WHERE u.id is "{g.user['id']}" ORDER BY created DESC').fetchall()
	graph_weights = db.execute(f'SELECT weight FROM weight w JOIN user u on w.author_id = u.id WHERE u.id is "{g.user['id']}" ORDER BY created DESC').fetchall()

	fig = plt.figure(figsize=(10, 6))

	plt.plot(graph_time, graph_weights, c='black')
	
	plt.xlabel("Time", fontsize=10)
	plt.ylabel("Weight", fontsize=10)

	fig.autofmt_xdate()

	# plt.figure(figsize=(50, 50))

	plt.tick_params(axis='both', which='major', labelsize=10)
	
	plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f kg'))

	plt.savefig('openbook/static/weights.png', bbox_inches='tight')

	return render_template('weight/index.html', weights=weights)

@login_required
@bp.route('/weight/new', methods=('GET', 'POST'))
def new():

	if request.method == 'POST':
		weight = request.form['weight']
		comment  = request.form['comment']
		error = None

		if not weight:
			error = 'Weight is required.'
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute('INSERT INTO weight (weight, comment, author_id) VALUES (?, ?, ?)', (weight, comment, g.user['id']))
			db.commit()
			return redirect(url_for('weight.index'))

	return render_template('weight/new.html')


