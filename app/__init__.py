from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail
from twilio.rest import Client

db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.update(dict(MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_DEFAULT_SENDER = 'conmiscotusca2@gmail.com', 
        MAIL_USERNAME = 'conmiscotusca2@gmail.com', 
        MAIL_PASSWORD = 'nnbo fxec wqvd dvaa' ))
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    
    client = Client(account_sid, auth_token)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    mail.init_app(app)

    db.init_app(app)
    
    # Registrar los blueprints sin prefix

    return app