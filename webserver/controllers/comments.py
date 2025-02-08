from flask import render_template, request, redirect, url_for, session
from .main import app
from webserver.models import Comments


@app.route('/threads/<int:thread_id>/comments/create', methods=('GET', 'POST'))
def create_comment(thread_id):
    user_id = session.get('user_id')
    if user_id is None: return redirect(url_for('auth'))

    if request.method == 'POST':
        comment_text = request.form.get('comment_text')

        Comments.create_comment(thread_id, user_id, comment_text)

        return redirect(url_for('get_thread', thread_id=thread_id))

    return render_template('comments/create.html', thread_id=thread_id)


@app.route('/threads/<int:thread_id>/comments/<int:comment_id>/edit', methods=('GET', 'POST'))
def edit_comment(thread_id, comment_id):
    if not (Comments.get_comment(comment_id)['user_id'] == session.get('user_id')):
        return redirect(url_for('auth'))

    if request.method == 'POST':
        comment_text = request.form.get('comment_text')

        Comments.edit_comment(comment_id, comment_text)

        return redirect(url_for('get_thread', thread_id=thread_id))

    return render_template('comments/edit.html', comment=Comments.get_comment(comment_id))


@app.route('/threads/<int:thread_id>/comments/<int:comment_id>/delete', methods=('POST',))
def delete_comment(thread_id, comment_id):
    if not (
        'Thread moderation' in session.get('permissions') or
        Comments.get_comment(comment_id)['user_id'] == session.get('user_id')
    ): return redirect(url_for('auth'))

    Comments.delete_comment(comment_id)
    return redirect(url_for('get_thread', thread_id=thread_id))
