from flask import Flask
from api1.app import api1_blueprint
from api2.app import api2_blueprint
import os

# Crea una única aplicación de Flask
combined_app = Flask(__name__)

# Registra los Blueprints con prefijos de URL
combined_app.register_blueprint(api1_blueprint, url_prefix='/api1')
combined_app.register_blueprint(api2_blueprint, url_prefix='/api2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Toma el puerto del entorno
    combined_app.run(host='0.0.0.0', port=port)