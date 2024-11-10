# Mueve las importaciones dentro del bloque condicional
if __name__ == "__main__":
    from app import create_app, db  # Importa create_app y db aquí

    # Crear la instancia de la aplicación Flask
    app = create_app()

    # Crear las tablas en la base de datos (si aún no se han creado)
    with app.app_context():
        db.create_all()  # Esto crea las tablas definidas en tus modelos

    # Iniciar la aplicación Flask
    app.run(debug=True, host='0.0.0.0', port=5000)