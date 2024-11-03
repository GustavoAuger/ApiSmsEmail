from flask import Flask, jsonify, request
from flask_mail import Mail, Message
import oracledb
import os
import requests

app = Flask(__name__)

def get_db_connection():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))         # Inicializa el cliente Oracle# Ruta base del proyecto, partiendo desde el archivo actual
        # Configura el entorno TNS_ADMIN
        wallet_path = os.path.join(BASE_DIR, "..", "oracle", "wallet")
        os.environ['TNS_ADMIN'] = wallet_path
        print("TNS_ADMIN:", os.environ.get('TNS_ADMIN'))
		
        try:
            oracle_client_path = os.path.join(BASE_DIR, "..", "oracle", "instantclient_23_4")
            oracledb.init_oracle_client(lib_dir=oracle_client_path)
            print("Cliente Oracle inicializado")
        except Exception as e:
            print("Error al inicializar el cliente Oracle:", e)
            return None

        # Crear DSN usando los detalles extraídos
        dsn_tns = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST=adb.sa-santiago-1.oraclecloud.com)(PORT=1522))(CONNECT_DATA=(service_name=gd82dea65a36163_mxyz2s5ivm0hivkf_high.adb.oraclecloud.com)))"
        print("DSN creado:", dsn_tns)

        # Conecta usando usuario, contraseña y DSN
        connection = oracledb.connect(
            user='SEGURITO1',
            password='SEGUR222.PRUEBA_a1',
            dsn=dsn_tns
        )
        print("Conexión establecida con éxito")
        return connection
    
    except oracledb.DatabaseError as e:
        print("Error de conexión:", e)
        return None


# Configuración del servidor de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com' # Cambia al servidor SMTP que uses
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'conmiscotusca2@gmail.com'  # correo de salida
app.config['MAIL_PASSWORD'] = 'nnbo fxec wqvd dvaa' 
mail = Mail(app)

# Función para obtener la lista de "no molestar" desde la Mock API

NO_MOLESTAR_API_URL = 'https://672258a92108960b9cc41077.mockapi.io/api/nomolestar/email'

def obtener_lista_no_molestar():
    try:
        response = requests.get(NO_MOLESTAR_API_URL)
        if response.status_code == 200:
            lista_no_molestar = response.json()
            return [usuario["email"] for usuario in lista_no_molestar]
        else:
            print("Error al consultar la API de 'No molestar'")
            return []
    except requests.RequestException as e:
        print("Error en la conexión con la API de 'No molestar':", e)
        return []

# Función para obtener destinatarios por ID de campaña
def obtener_destinatarios(id_campana):
    connection = get_db_connection()
    destinatarios = []

    try:
        cursor = connection.cursor()
        query = """
            SELECT nombre, email 
            FROM destinatario
            WHERE campanaid = :id_campana
        """
        cursor.execute(query, [id_campana])
        rows = cursor.fetchall()

        # Almacena en el diccionario
        for row in rows:
            destinatarios.append({"nombre": row[0], "email": row[1]})

    except oracledb.DatabaseError as e:
        print("Error en la consulta:", e)
    finally:
        cursor.close()
        connection.close()

    return destinatarios
	

# API para enviar correos según el id de campaña
@app.route('/api/send-emails', methods=['POST'])
def send_emails():
    data = request.json
    id_campana = data.get('id_campana')

    if not id_campana:
        return jsonify({"error": "Falta el ID de la campaña"}), 400

    # Paso 1: Obtiene los destinatarios de la campaña desde la base de datos
    destinatarios = obtener_destinatarios(id_campana)
    
    if not destinatarios:
        return jsonify({"error": "No se encontraron destinatarios para esta campaña"}), 404

    # Paso 2: Obtiene la lista de correos de "no molestar" desde la Mock API
    no_molestar = obtener_lista_no_molestar()

    # Filtra los destinatarios, excluyendo aquellos en la lista de "no molestar"
    destinatarios = [d for d in destinatarios if d['email'] not in no_molestar]

    # Paso 3: Envía los correos a los destinatarios filtrados
    enviados = []
    errores = []

    for destinatario in destinatarios:
        nombre = destinatario['nombre']
        email = destinatario['email']
        subject = f"Hola, {nombre}! Aquí está tu mensaje personalizado"
        body = f"Estimado/a {nombre}, este es un mensaje personalizado para ti."

        msg = Message(subject=subject,
                      recipients=[email],
                      body=body,
                      sender=app.config['MAIL_USERNAME'])

        try:
            mail.send(msg)
            enviados.append({"nombre": nombre, "email": email})
        except Exception as e:
            errores.append({"nombre": nombre, "email": email, "error": str(e)})

    return jsonify({"enviados": enviados, "errores": errores}), 200

#if __name__ == '__main__':
   # app.run(port=5000)
