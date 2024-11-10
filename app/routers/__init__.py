from flask import Flask
from .user import user_bp
from .campaign import campaign_bp
from .report import report_bp
from .envio import envio_bp

def create_app():
    app = Flask(__name__)
    
    # Registrar los blueprints sin prefix
    app.register_blueprint(user_bp)
    app.register_blueprint(campaign_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(envio_bp)
    
    return app