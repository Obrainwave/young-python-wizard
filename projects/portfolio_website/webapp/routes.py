from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    projects = current_app.config['PROJECT_SERVICE'].get_all_projects()
    return render_template('index.html', projects=projects)

@main.route('/project/<int:project_id>')
def project_detail(project_id):
    project = current_app.config['PROJECT_SERVICE'].get_project(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('main.index'))
    return render_template('project_detail.html', project=project)

@main.route('/admin')
def admin():
    projects = current_app.config['PROJECT_SERVICE'].get_all_projects()
    return render_template('admin.html', projects=projects)

@main.route('/admin/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        try:
            project = current_app.config['PROJECT_SERVICE'].create_project(
                title=request.form['title'],
                description=request.form['description'],
                image_url=request.form.get('image_url', ''),
                github_url=request.form.get('github_url', ''),
                live_url=request.form.get('live_url', ''),
                date_created=request.form.get('date_created', ''),
                featured='featured' in request.form
            )
            flash('Project added successfully!', 'success')
            return redirect(url_for('main.admin'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('edit_project.html', project=None)

@main.route('/admin/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = current_app.config['PROJECT_SERVICE'].get_project(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('main.admin'))
    if request.method == 'POST':
        try:
            updated = current_app.config['PROJECT_SERVICE'].update_project(
                project_id=project_id,
                title=request.form['title'],
                description=request.form['description'],
                image_url=request.form.get('image_url', ''),
                github_url=request.form.get('github_url', ''),
                live_url=request.form.get('live_url', ''),
                date_created=request.form.get('date_created', ''),
                featured='featured' in request.form
            )
            flash('Project updated successfully!', 'success')
            return redirect(url_for('main.admin'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('edit_project.html', project=project)

@main.route('/admin/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if current_app.config['PROJECT_SERVICE'].delete_project(project_id):
        flash('Project deleted.', 'success')
    else:
        flash('Project not found.', 'error')
    return redirect(url_for('main.admin'))