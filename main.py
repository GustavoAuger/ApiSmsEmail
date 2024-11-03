from flask import Flask
from api1.app import app as api1_app
from api2.app import app as api2_app

combined_app = Flask(__name__)

# Registrar api1 y api2 en la aplicación combinada usando blueprints
combined_app.register_blueprint(api1_app, url_prefix='/api1')
combined_app.register_blueprint(api2_app, url_prefix='/api2')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Usar el puerto del entorno o 5000 por defecto
    combined_app.run(host='0.0.0.0', port=port)