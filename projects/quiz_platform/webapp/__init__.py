from flask import Flask
from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.quiz_service import QuizService
from services.attempt_service import AttemptService


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-in-production"
    db_path = "quiz.db"

    # Initialize schema
    db = Database(db_path)
    db.connect()
    DatabaseInitializer(db).initialize()
    db.close()

    # Services
    app.config["QUIZ_SERVICE"] = QuizService(db_path)
    app.config["ATTEMPT_SERVICE"] = AttemptService(db_path)

    # Blueprints
    from webapp.routes import main
    from webapp.admin_routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix="/admin")

    return app