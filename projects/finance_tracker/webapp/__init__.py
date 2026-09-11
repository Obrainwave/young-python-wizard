from flask import Flask
from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.account_service import AccountService
from services.category_service import CategoryService
from services.transaction_service import TransactionService
from services.budget_service import BudgetService


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-in-production"
    db_path = "finance.db"

    # Initialize schema
    db = Database(db_path)
    db.connect()
    DatabaseInitializer(db).initialize()
    db.close()

    # Register services
    app.config["ACCOUNT_SERVICE"] = AccountService(db_path)
    app.config["CATEGORY_SERVICE"] = CategoryService(db_path)
    app.config["TRANSACTION_SERVICE"] = TransactionService(db_path)
    app.config["BUDGET_SERVICE"] = BudgetService(db_path)

    # Register blueprints
    from webapp.routes.main_routes import main
    from webapp.routes.account_routes import accounts_bp
    from webapp.routes.category_routes import categories_bp
    from webapp.routes.transaction_routes import transactions_bp
    from webapp.routes.budget_routes import budgets_bp

    app.register_blueprint(main)
    app.register_blueprint(accounts_bp, url_prefix="/accounts")
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(budgets_bp, url_prefix="/budgets")

    return app