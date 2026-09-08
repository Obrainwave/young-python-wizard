from flask import Flask, g
from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.project_service import ProjectService

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['DB_PATH'] = 'portfolio.db'

    # Initialize database schema once
    db = Database(app.config['DB_PATH'])
    db.get_connection()
    DatabaseInitializer(db).initialize()
    db.close()

    # Register request handlers
    @app.before_request
    def before_request():
        g.db = Database(app.config['DB_PATH'])
        g.db.connect()

    @app.teardown_request
    def teardown_request(exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    # Store a function to get the current connection
    def get_db():
        return g.db

    # Create service with a function that returns current connection
    # We'll modify repositories to accept a connection getter.
    service = ProjectService(get_db)

    app.config['PROJECT_SERVICE'] = service

    from webapp.routes import main
    app.register_blueprint(main)

    return app