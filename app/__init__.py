from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app import config
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    

    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    mail.init_app(app)

    # Initialize extensions
    db.init_app(app)

    #from .routes import main as main_blueprint
    #app.register_blueprint(main_blueprint)

    return app

