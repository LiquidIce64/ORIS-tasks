from flask import render_template, request, redirect, url_for
from .main import app
from .utils import check_permission
from webserver.models import Tags


@app.route('/tags')
@check_permission('Tag editing')
def get_tags():
    return render_template('tags/tags.html', tags=Tags.get_tags())


@app.route('/tags/create', methods=('GET', 'POST'))
@check_permission('Tag editing')
def create_tag():
    if request.method == 'POST':
        tag_name = request.form.get('tag_name')
        tag_color = request.form.get('tag_color')

        Tags.create_tag(tag_name, tag_color)

        return redirect(url_for('get_tags'))

    return render_template('tags/create.html')


@app.route('/tags/<int:tag_id>/edit', methods=('GET', 'POST'))
@check_permission('Tag editing')
def edit_tag(tag_id):
    if request.method == 'POST':
        tag_name = request.form.get('tag_name')
        tag_color = request.form.get('tag_color')

        Tags.edit_tag(tag_id, tag_name, tag_color)

        return redirect(url_for('get_tags'))

    return render_template('tags/edit.html', tag=Tags.get_tag(tag_id))


@app.route('/tags/<int:tag_id>/delete', methods=('POST',))
@check_permission('Tag editing')
def delete_tag(tag_id):
    Tags.delete_tag(tag_id)
    return redirect(url_for('get_tags'))
