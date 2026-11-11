from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # Basic config (for teaching/demo purposes)
    app.config["SECRET_KEY"] = "devkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "main_routes.login"

    # Import routes
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app