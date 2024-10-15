from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from openbook.auth import login_required
from openbook.db import get_db

bp = Blueprint('blog', __name__)

# if g.user:

@bp.route('/blog', methods=('GET', 'POST'))
@login_required
def index():
# select * from comment where post_id is x ORDER BY created DESC
    if request.method == 'POST':
        comment = request.form['comment']
        post_id = request.form['post_id']
        error = None

        if not comment:
            error = 'Comment is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (body, author_id, post_id)'
                ' VALUES (?, ?, ?)',
                (comment, g.user['id'], post_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    # comments = db.execute(
    #     'SELECT c.id, body, created, author_id, username'
    #     ' FROM comment c JOIN user u ON c.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    length = db.execute('select count(*) from post').fetchone()[0]

    listofcomments = [''] * (length + 1)
    # listofcomments = []

    for i in range(length + 1):
        listofcomments[i] = db.execute(
                f'select c.id, c.body, c.created, c.author_id, post_id, username from comment c join user u on c.author_id = u.id where post_id is {i}'
            ).fetchall()

    return render_template('blog/index.html', posts=posts, listofcomments=listofcomments)

@bp.route('/blog/post/<int:id>', methods=('GET', 'POST'))
def post(id):

    if request.method == 'POST':
        comment = request.form['comment']
        post_id = request.form['post_id']
        error = None

        if not comment:
            error = 'Comment is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (body, author_id, post_id)'
                ' VALUES (?, ?, ?)',
                (comment, g.user['id'], post_id)
            )
            db.commit()
            # return redirect(url_for('blog.index.post.id'))
            return redirect(f'/blog/post/{id}')

    posts = [get_post(id, check_author=False)]

    db = get_db()

    length = db.execute('select count(*) from post').fetchone()[0]

    listofcomments = [None] * (length + 1)

    listofcomments[id] = db.execute(
                f'select c.id, c.body, c.created, c.author_id, post_id, username from comment c join user u on c.author_id = u.id where post_id is {id}'
            ).fetchall()
    
    return render_template('blog/index.html', posts=posts, listofcomments=listofcomments)

@bp.route('/blog/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body  = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/blog/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# @bp.route('/blog/delete/<int:id>', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     # Turn Invisible
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))
