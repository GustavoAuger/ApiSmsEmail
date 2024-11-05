from app import create_app, db
from app.routes import user_bp

# Create the Flask application instance
app = create_app()

# Create the tables in the database
with app.app_context():
    db.create_all()  # This creates the tables defined in your models

app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)