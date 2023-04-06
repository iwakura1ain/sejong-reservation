from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import *

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    cur = get_cur()
    
    cur.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM Post p JOIN User u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )

    try:
        posts = []
        for p in cur.fetchall():
            posts.append({"id": p[0], "title": p[1], "body": p[2], "created": p[3], "author_id": p[4], "username": p[5]})
    except TypeError:
        return render_template('index.html', posts=[])
    
    #print(f"posts: {posts}")
    return render_template('index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:

            print(f"g.user: {g.user}")
            db = get_db()
            cur = get_cur()
            cur.execute(
                'INSERT INTO Post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                #(title, body, g.user['id'])
                (title, body, g.user[0])
            )
            
            return redirect(url_for('blog.index'))

    return render_template('create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
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
            cur = get_cur()
            cur.execute(
                'UPDATE Post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            
            return redirect(url_for('blog.index'))

    return render_template('update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    cur = get_cur()
    cur.execute('DELETE FROM Post WHERE id = ?', (id,))
    
    return redirect(url_for('blog.index'))


def get_post(id, check_author=True):
    db = get_db()
    cur = get_cur()

    cur.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM Post p JOIN User u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    )

    p = cur.fetchone()
    post = {"id": p[0], "title": p[1], "body": p[2], "created": p[3], "author_id": p[4], "username": p[5]}
    #print(f"post: {post}")

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    #if check_author and post['author_id'] != g.user['id']:
    if check_author and post['author_id'] != g.user[0]:
        abort(403)

    return post
