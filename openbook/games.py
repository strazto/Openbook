from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from openbook.auth import login_required
from openbook.db import get_db

bp = Blueprint('games', __name__)

@bp.route('/game_index')
def index():
    db = get_db()
    games = db.execute(
        'SELECT p.id, title, developer, created, author_id, year, genres, series, vibes, tags, setting, country, platforms, image, username'
        ' FROM game p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('games/index.html', games=games)

@bp.route('/game_create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        developer = request.form['developer']
        year = request.form['year']
        genres = request.form['genres']
        series = request.form['series']
        vibes = request.form['vibes']
        tags = request.form['tags']
        setting = request.form['setting']
        country = request.form['country']
        platforms = request.form['platforms']
        image = request.form['image']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO game (title, developer, author_id, year, genres, series, vibes, tags, setting, country, platforms, image)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, developer, g.user['id'], year, genres, series, vibes, tags, setting, country, platforms, image)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('games/create.html')

# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM game p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post

# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     # Turn Invisible
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))
