from app import create_app, db
from app.user import user_bp
from app.campaign import campaign_bp
from app.report import report_bp
from app.envio import envio_bp

# Create the Flask application instance
app = create_app()

# Create the tables in the database
with app.app_context():
    db.create_all()  # This creates the tables defined in your models

app.register_blueprint(user_bp)
app.register_blueprint(campaign_bp)
app.register_blueprint(report_bp)
app.register_blueprint(envio_bp)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)