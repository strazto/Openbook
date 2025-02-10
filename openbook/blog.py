from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from openbook.auth import login_required
from openbook.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/blog', methods=('GET', 'POST'))
@bp.route('/blog/post/<int:id>', methods=('GET', 'POST'))
@bp.route('/blog/filter/<string:filter>', methods=('GET', 'POST'))
@login_required
def index(id = None, filter = None):
    if request.method == 'POST':
        if 'tag' in request.form:
            tag = request.form['tag']
            error = None

            if not tag:
                error = 'Tag is required'
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute('INSERT INTO tag (author_id, title) VALUES (?, ?)', (g.user['id'], tag))
                db.commit()
                return redirect(url_for('blog.index'))

        if 'comment' in request.form:
            comment = request.form['comment']
            post_id = request.form['post_id']
            error = None

            if not comment:
                error = 'Comment is required.'
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute('INSERT INTO comment (body, author_id, post_id) VALUES (?, ?, ?)', (comment, g.user['id'], post_id))
                db.commit()
                return redirect(url_for('blog.index', id=id))

        if 'title' in request.form:
            title = request.form['title']
            body  = request.form['body']
            error = None

            if not title:
                error = 'Title is required.'
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute('INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)', (title, body, g.user['id']))
                db.commit()
                return redirect(url_for('blog.index', id=id))

    db = get_db()

    posts = None

    if filter:
        posts = db.execute(f'select post.created, post.title, post.id, post.body, user.username from tag join post_tag on tag.id = tag_id join post on post.id = post_id join user on user.id = post.author_id where tag.title is "{filter}" ORDER BY post.created DESC').fetchall()
    elif id:
        posts = [get_post(id, check_author=False)]
    else:
        posts = db.execute('SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC').fetchall()

    length = db.execute('select count(*) from post').fetchone()[0]

    listofcomments = [''] * (length + 1)
    tag_list = [''] * (length + 1)

    for i in range(length + 1):
        listofcomments[i] = db.execute(f'select c.id, c.body, c.created, c.author_id, post_id, username from comment c join user u on c.author_id = u.id where post_id is {i}').fetchall()
        tag_list[i] = db.execute(f'select title from post_tag join tag on tag_id = tag.id where post_id is {i}').fetchall()

    tags = db.execute('SELECT title FROM tag ORDER BY title ASC').fetchall()

    return render_template('blog/index.html', posts=posts, listofcomments=listofcomments, tags=tags, tag_list=tag_list)

@bp.route('/blog/create', methods=('GET', 'POST'))
@bp.route('/blog/update/<int:id>', methods=('GET', 'POST'))
@login_required
def create(id = None, post = None, tags = None, tag_list = None):

    if request.method == 'POST':
        title = request.form['title']
        body  = request.form['body']
        
        if 'tag' in request.form:
            tag   = request.form['tag']
            # flash(tag)

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
 
            if id:
                db.execute('UPDATE post SET title = ?, body = ? WHERE id = ?', (title, body, id))
            
            else:
                db.execute('INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)', (title, body, g.user['id']))

            if not id:
                id = db.execute('SELECT count(*) from post').fetchone()[0]

            if tag:
                db.execute('INSERT INTO post_tag (post_id, tag_id) VALUES (?, ?)', (id, tag))

            db.commit()
            return redirect(url_for('blog.index', id=id))

    if id:
        post = get_post(id)

    db = get_db()

    tags = db.execute('SELECT id, title FROM tag ORDER BY created ASC').fetchall()
    # surely can optimise this such that only sends a list of tags that are not already selected, in SQL

    if id:
        tag_list = db.execute(f'SELECT title FROM post_tag join tag on tag_id = tag.id where post_id is {id}').fetchall()

    return render_template('blog/create.html', post=post, tags=tags, tag_list = tag_list)

def get_post(id, check_author=True):
    post = get_db().execute('SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?', (id,)).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

# def handle_form(request):
#     if request.method == 'POST':
#         title = request.form['title']
#         body  = request.form['body']
#         tag   = request.form['tag']
#         error = None

#         flash(tag)

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
#             if tag:
#                 db.execute(
#                     'INSERT INTO post_tag (post_id, tag_id)'
#                     ' VALUES (?, ?)',
#                     (id, tag)
#                 )

#             db.commit()
#             return redirect(url_for('blog.index'))

# @bp.route('/blog/delete/<int:id>', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     # Turn Invisible
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))
