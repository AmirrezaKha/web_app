from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import time
from sqlalchemy.exc import OperationalError

import os
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'createapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User  # Import here, after initializing db

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Create the database tables
    with app.app_context():
        for _ in range(5):
            try:
                db.create_all()  # Create tables
                break  # Break the loop if successful
            except OperationalError:
                time.sleep(5)  # Wait for 5 seconds before retrying

    return app
