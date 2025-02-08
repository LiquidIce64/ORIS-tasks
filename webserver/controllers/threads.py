from flask import render_template, request, redirect, url_for, session
from .main import app
from webserver.models import Threads, Comments, Tags


@app.route('/threads')
def get_threads():
    return render_template('threads/threads.html', threads=[(
        thread,
        Tags.get_thread_tags(thread['id'])
    ) for thread in Threads.get_threads()])


@app.route('/threads/<int:thread_id>')
def get_thread(thread_id):
    return render_template(
        'threads/thread.html',
        thread=Threads.get_thread(thread_id),
        tags=Tags.get_thread_tags(thread_id),
        comments=[(
            comment,
            session.get('user_id') is not None and comment['user_id'] == session.get('user_id'),
            session.get('user_id') is not None and 'Thread moderation' in session.get('permissions')
        ) for comment in Comments.get_comments(thread_id)],
        show_actions=session.get('user_id') is not None and (
            'Thread moderation' in session.get('permissions') or
            Threads.get_thread(thread_id)['author_id'] == session.get('user_id')
        )
    )


@app.route('/threads/create', methods=('GET', 'POST'))
def create_thread():
    user_id = session.get('user_id')
    if user_id is None: return redirect(url_for('auth'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.getlist('tags', type=int)

        thread_id = Threads.create_thread(user_id, title, description, tags)

        return redirect(url_for('get_thread', thread_id=thread_id))

    return render_template('threads/create.html', tags=Tags.get_tags())


@app.route('/threads/<int:thread_id>/edit', methods=('GET', 'POST'))
def edit_thread(thread_id):
    if not (
        'Thread moderation' in session.get('permissions') or
        Threads.get_thread(thread_id)['author_id'] == session.get('user_id')
    ): return redirect(url_for('auth'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.getlist('tags', type=int)

        Threads.edit_thread(thread_id, title, description, tags)

        return redirect(url_for('get_thread', thread_id=thread_id))

    return render_template(
        'threads/edit.html',
        thread=Threads.get_thread(thread_id),
        thread_tags=Tags.get_thread_tags(thread_id),
        tags=Tags.get_tags()
    )


@app.route('/threads/<int:thread_id>/delete', methods=('POST',))
def delete_thread(thread_id):
    if not (
        'Thread moderation' in session.get('permissions') or
        Threads.get_thread(thread_id)['author_id'] == session.get('user_id')
    ): return redirect(url_for('auth'))

    Threads.delete_thread(thread_id)
    return redirect(url_for('get_threads'))
