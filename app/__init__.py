from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "home.login"


def create_app(config="app.config.ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    db_migrate.init_app(app, db, directory="app/db/migrations")
    mail.init_app(app)
    login_manager.init_app(app)

    # Import & Register Blueprints
    from app.views.home import home

    app.register_blueprint(home)

    return app
