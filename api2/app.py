from flask import Flask, jsonify, request
from twilio.rest import Client
import oracledb
import os

app = Flask(__name__)

# Configuración de Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = '+16502002145'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_db_connection():
    try:
        # Configura el entorno TNS_ADMIN
        os.environ['TNS_ADMIN'] = 'D:/programas/Segurito/wallet'
        print("TNS_ADMIN:", os.environ.get('TNS_ADMIN'))

        # Inicializa el cliente Oracle
        try:
            oracledb.init_oracle_client(lib_dir=r"D:/oracle/instantclient_23_4")
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


def obtener_destinatarios_sms(id_campana):
    connection = get_db_connection()  # Solo obtén la conexión
    destinatarios = []

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return destinatarios  # Retorna la lista vacía si no se puede conectar

    try:
        cursor = connection.cursor()
        # Consulta para obtener los destinatarios con el código de campaña
        query = """
            SELECT nombre, telefono
            FROM destinatario
            WHERE campanaid = :id_campana
        """
        cursor.execute(query, {'id_campana': id_campana})  # Cambia 'codigo' por 'id_campana'
        rows = cursor.fetchall()

        # Almacena en el diccionario
        for row in rows:
            destinatarios.append({"nombre": row[0], "telefono": row[1]})

    except oracledb.DatabaseError as e:
        print("Error en la consulta:", e)
    finally:
        cursor.close()
        connection.close()  # Cierra la conexión

    return destinatarios



@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    # Obtener el código de campaña del cuerpo de la solicitud
    data = request.get_json()
    id_campana = data.get('id_campana')
    
    if not id_campana:
        return jsonify({'error': 'Debe proporcionar un código de campaña'}), 400
    
    try:
        # Obtener la lista de destinatarios desde la base de datos
        destinatarios = obtener_destinatarios_sms(id_campana)
        
        if not destinatarios:
            return jsonify({'status': f'No hay destinatarios para el código de campaña {id_campana}'}), 200

        mensajes_enviados = []
        
        for destinatario in destinatarios:
            numero_destino = destinatario['telefono']
            nombre_destinatario = destinatario['nombre']
            # Enviar el SMS con el nombre del destinatario
            message = client.messages.create(
                body=f"Hola {nombre_destinatario}, este es un mensaje de prueba desde la API SMS",
                from_=TWILIO_PHONE_NUMBER,
                to=numero_destino
            )
            mensajes_enviados.append({'nombre': nombre_destinatario, 'numero': numero_destino, 'sid': message.sid})
        
        return jsonify({'status': 'SMS enviados', 'mensajes': mensajes_enviados}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#if __name__ == '__main__':
 #   app.run(debug=True)
