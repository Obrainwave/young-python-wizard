from flask import Flask
from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    db_path = 'student_management.db'

    # Initialize database schema
    db = Database(db_path)
    db.connect()
    DatabaseInitializer(db).initialize()
    db.close()

    # Create services
    app.config['STUDENT_SERVICE'] = StudentService(db_path)
    app.config['COURSE_SERVICE'] = CourseService(db_path)
    app.config['ENROLLMENT_SERVICE'] = EnrollmentService(db_path)

    from webapp.routes import main
    app.register_blueprint(main)

    return app