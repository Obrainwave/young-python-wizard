from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

main = Blueprint('main', __name__)

# ========== HOME ==========
@main.route('/')
def index():
    return render_template('index.html')

# ========== STUDENT ROUTES ==========
@main.route('/students')
def list_students():
    search = request.args.get('search', '')
    if search:
        students = current_app.config['STUDENT_SERVICE'].search_students(search)
    else:
        students = current_app.config['STUDENT_SERVICE'].get_all_students()
    return render_template('students.html', students=students, search=search)

@main.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            current_app.config['STUDENT_SERVICE'].create_student(
                name=request.form['name'],
                email=request.form.get('email', ''),
                phone=request.form.get('phone', '')
            )
            flash('Student added successfully!', 'success')
            return redirect(url_for('main.list_students'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('student_form.html', student=None)

@main.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = current_app.config['STUDENT_SERVICE'].get_student(student_id)
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('main.list_students'))
    if request.method == 'POST':
        try:
            current_app.config['STUDENT_SERVICE'].update_student(
                student_id=student_id,
                name=request.form['name'],
                email=request.form.get('email', ''),
                phone=request.form.get('phone', '')
            )
            flash('Student updated!', 'success')
            return redirect(url_for('main.list_students'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('student_form.html', student=student)

@main.route('/students/<int:student_id>')
def student_detail(student_id):
    student = current_app.config['STUDENT_SERVICE'].get_student(student_id)
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('main.list_students'))
    enrollments = current_app.config['ENROLLMENT_SERVICE'].get_enrollments_by_student(student_id)
    return render_template('student_detail.html', student=student, enrollments=enrollments)

@main.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if current_app.config['STUDENT_SERVICE'].delete_student(student_id):
        flash('Student deleted.', 'success')
    else:
        flash('Student not found.', 'error')
    return redirect(url_for('main.list_students'))

# ========== COURSE ROUTES ==========
@main.route('/courses')
def list_courses():
    search = request.args.get('search', '')
    if search:
        courses = current_app.config['COURSE_SERVICE'].search_courses(search)
    else:
        courses = current_app.config['COURSE_SERVICE'].get_all_courses()
    return render_template('courses.html', courses=courses, search=search)

@main.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        try:
            current_app.config['COURSE_SERVICE'].create_course(
                title=request.form['title'],
                description=request.form.get('description', ''),
                credits=int(request.form.get('credits', 0))
            )
            flash('Course added successfully!', 'success')
            return redirect(url_for('main.list_courses'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('course_form.html', course=None)

@main.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = current_app.config['COURSE_SERVICE'].get_course(course_id)
    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('main.list_courses'))
    if request.method == 'POST':
        try:
            current_app.config['COURSE_SERVICE'].update_course(
                course_id=course_id,
                title=request.form['title'],
                description=request.form.get('description', ''),
                credits=int(request.form.get('credits', 0))
            )
            flash('Course updated!', 'success')
            return redirect(url_for('main.list_courses'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('course_form.html', course=course)

@main.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = current_app.config['COURSE_SERVICE'].get_course(course_id)
    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('main.list_courses'))
    enrollments = current_app.config['ENROLLMENT_SERVICE'].get_enrollments_by_course(course_id)
    return render_template('course_detail.html', course=course, enrollments=enrollments)

@main.route('/courses/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if current_app.config['COURSE_SERVICE'].delete_course(course_id):
        flash('Course deleted.', 'success')
    else:
        flash('Course not found.', 'error')
    return redirect(url_for('main.list_courses'))

# ========== ENROLLMENT ROUTES ==========
@main.route('/enrollments')
def list_enrollments():
    enrollments = current_app.config['ENROLLMENT_SERVICE'].get_all_enrollments()
    return render_template('enrollments.html', enrollments=enrollments)

@main.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    students = current_app.config['STUDENT_SERVICE'].get_all_students()
    courses = current_app.config['COURSE_SERVICE'].get_all_courses()
    if request.method == 'POST':
        try:
            current_app.config['ENROLLMENT_SERVICE'].enroll_student(
                student_id=int(request.form['student_id']),
                course_id=int(request.form['course_id']),
                grade=request.form.get('grade', ''),
                enrolled_on=request.form.get('enrolled_on', '')
            )
            flash('Enrollment added successfully!', 'success')
            return redirect(url_for('main.list_enrollments'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('enrollment_form.html', enrollment=None, students=students, courses=courses)

@main.route('/enrollments/edit/<int:enrollment_id>', methods=['GET', 'POST'])
def edit_enrollment(enrollment_id):
    enrollment = current_app.config['ENROLLMENT_SERVICE'].get_enrollment(enrollment_id)
    if not enrollment:
        flash('Enrollment not found.', 'error')
        return redirect(url_for('main.list_enrollments'))
    students = current_app.config['STUDENT_SERVICE'].get_all_students()
    courses = current_app.config['COURSE_SERVICE'].get_all_courses()
    if request.method == 'POST':
        try:
            current_app.config['ENROLLMENT_SERVICE'].update_enrollment(
                enrollment_id=enrollment_id,
                student_id=int(request.form['student_id']),
                course_id=int(request.form['course_id']),
                grade=request.form.get('grade', ''),
                enrolled_on=request.form.get('enrolled_on', '')
            )
            flash('Enrollment updated!', 'success')
            return redirect(url_for('main.list_enrollments'))
        except ValueError as e:
            flash(str(e), 'error')
    return render_template('enrollment_form.html', enrollment=enrollment, students=students, courses=courses)

@main.route('/enrollments/delete/<int:enrollment_id>', methods=['POST'])
def delete_enrollment(enrollment_id):
    if current_app.config['ENROLLMENT_SERVICE'].delete_enrollment(enrollment_id):
        flash('Enrollment deleted.', 'success')
    else:
        flash('Enrollment not found.', 'error')
    return redirect(url_for('main.list_enrollments'))