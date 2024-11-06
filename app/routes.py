from flask import Blueprint, jsonify, request,app
from .models2 import User,Campana,Envio,Envio_destinatario,Destinatario
from flask_mail import Message
import supabase,os
from supabase import Client,create_client
from werkzeug.security import generate_password_hash, check_password_hash
from . import create_app,mail
from twilio.rest import Client


user_bp = Blueprint('user', __name__)

url = 'https://zwcokbhciyalafyflvkc.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3Y29rYmhjaXlhbGFmeWZsdmtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4OTMzODYsImV4cCI6MjA0NTQ2OTM4Nn0.QWNxXN5_rCDmPNaNpDDHpi5ws4su5XbM8s4ChlhrDGA'
supabase: Client = create_client(url, key)

############################ USUARIO
@user_bp.route('/list_users', methods=['GET'])
def fetch_users():
    user_id = request.args.get('id')
    response = supabase.table("User").select("*").eq("id", user_id).execute()

    if response.data:
        return jsonify(response.data), 200
        print("Response:", response)
    else:
        return jsonify("No se pudo traer a los usuarios"), 500
        print("Response:", response)

@user_bp.route('/add_user', methods=['POST'])
def create_user():
    data = request.json
    password = request.json.get('password')
    hashed_password = generate_password_hash(password)  
    data['password'] = hashed_password 
    user = User(**data)  # Create a User instance
    response = supabase.table("User").insert(data).execute()
    if response.data:
        return jsonify(response.data), 200
        print("Response:", response)
    else:
        return jsonify("No se pudo traer a los usuarios"), 500
        print("Response:", response)

@user_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    user_id = data.get("id")  # Extract user ID from the JSON payload
    if not user_id:
        return {"error": "User ID is required"}
      
    response = supabase.table("User").delete().eq("id", user_id).execute()
    if response.data:
        return jsonify(response.data), 200
        print("Response:", response)
    else:
        return jsonify("No se pudo borrar el usuario"), 500
        print("Response:", response)

@user_bp.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    # Check if the request body has valid data
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # If a password is provided, hash it
    if 'password' in data:
        password = data.get('password')
        hashed_password = generate_password_hash(password)
        data['password'] = hashed_password  # Update data with hashed password

    # Update the user in the Supabase table
    response = supabase.table("User").update(data).eq('id', user_id).execute()

    if response.data:
        return jsonify(response.data), 200
    else:
        return jsonify({"error": "Could not update user"}), 500
    
#######################CAMPAÑA############################################################
########################################################################################
@user_bp.route('/list_campaigns', methods=['GET'])
def fetch_campaigns():
    response = supabase.table("Campaña").select("*").execute()

    if response.data:
        return jsonify(response.data), 200
    else:
        return jsonify({"error": "No se pudo traer las campañas"}), 500
    
#######################CAMPAÑA POR ID############################################################
@user_bp.route('/list_campaigns_by_id', methods=['GET'])
def fetch_campaigns_by_id():
    user_id = request.args.get('user_id')
    canal = request.args.get('canal')

    if not user_id:
        return jsonify({"error": "Se necesita ID de usuario"}), 400
    if not canal:
        return jsonify({"error": "Se necesita canal"}), 400

    response = supabase.table("Campana").select("*").eq("user_id", user_id).eq("canal", canal).execute()

    if response.data:
        return jsonify(response.data), 200    
    
###########################################################3
###########################CREAR CAMPAÑA
@user_bp.route('/add_campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    campana = Campana(**data)  # Create a User instance
    response = supabase.table("Campana").insert(data).execute()
    if response.data:
        return jsonify(response.data), 200
        print("Response:", response)
    else:
        return jsonify("No se pudo registrar"), 500
        print("Response:", response)

##################################DESTINATARIOS###########3
##########################################################
@user_bp.route('/destinatarios_list', methods=['GET'])
def fetch_destinatarios():
    response = supabase.table("Destinatario").select("*").execute()
    if response.data:
        destinatarios = [response.data]
        return destinatarios
    else:
        return jsonify("No se pudo traer a los destinatarios"), 500
    
#############################################################
# ###################### GET ENVIOS ######################3    
@user_bp.route("/send_instances", methods=["GET"])
def get_envios_asociados_a_campana():
    campana_id = request.args.get('fk_id_campana')

    if not campana_id:
        return jsonify({"error": "ID DE CAMPAÑA ES REQUERIDA"}), 400
    
    try:
        response = supabase.table('Envio').select('*').eq('fk_id_campana', campana_id).execute()

        if response.data:
            return jsonify(response.data),200
        else:
            return jsonify({"error": "Failed to fetch data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
		
    #########################################################
    #################### GET TABLA INTERMEDIA################
@user_bp.route("/intermediary_records", methods=["GET"])
def get_intermediary_records_for_campaign():
    campana_id = request.args.get('fk_id_campana')

    if not campana_id:
        return jsonify({"error": "ID DE CAMPAÑA ES REQUERIDA"}), 400

    try:
        response = supabase.table('Envio').select('id_envio').eq('fk_id_campana', campana_id).execute()

        if not response.data:
            return jsonify({"error": "No se encontraron envíos para esta campaña."}), 400
        
        envio_ids = [envio['id_envio'] for envio in response.data]

        intermediary_response = supabase.table('Envio_destinatario') \
            .select('*') \
            .in_('fk_envio', envio_ids) \
            .execute()

        if not intermediary_response.data:
            return jsonify({"error": "No se encontraron registros intermediarios."}), 400
        
        recipient_ids = [record['fk_destinatario'] for record in intermediary_response.data]

        recipients_response = supabase.table('Destinatario') \
            .select('id_destinatario', 'nombre_destinatario', 'email') \
            .in_('id_destinatario', recipient_ids) \
            .execute()

        if recipients_response.data:
            result = []
            for record in intermediary_response.data:
                recipient = next((rec for rec in recipients_response.data if rec['id_destinatario'] == record['fk_destinatario']), None)
                if recipient:
                    result.append({
                        'Nombre': recipient['nombre_destinatario'],
                        'Email': recipient['email']
                    })

            return jsonify(result), 200
        else:
            return jsonify({"error": "No se encontraron destinatarios para los registros intermediarios."}), 400
            

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/send_campaign_emails", methods=["POST"])
def send_campaign_emails():
    email_data = request.json.get('email_data')

    if not email_data:
        return jsonify({"error": "Se necesitan destinatarios"}), 400

    try:
        sent_emails = []
        for email_info in email_data:
            email_destinatario = email_info['email']
            nombre_destinatario = email_info['nombre_destinatario']
            subject = f"HOLA ESTIMADO {nombre_destinatario} !!"
            body = f"CUERPO DE TU MENSAJE PARA CORREO: {email_destinatario} !!"

            # Create the email message
            message = Message(
                subject=subject,
                recipients=[email_destinatario],
                body=body
            )

            try:
                mail.send(message)
                sent_emails.append({
                    'recipient': nombre_destinatario,
                    'email': email_destinatario,
                    'status': 'ENVIADO'
                })
            except Exception as e:
                sent_emails.append({
                    'recipient': nombre_destinatario,
                    'email': email_destinatario,
                    'status': f'ERROR: {str(e)}'
                })

        return jsonify({'ENVIADOS': sent_emails}), 200

    except Exception as e:
        return jsonify({"ERROR": str(e)}), 500
    
############################################################
########################sms##############################
@user_bp.route('/send-sms', methods=['POST'])  # Change GET to POST
def send_sms_to_all():
    response = supabase.table('Destinatario').select('id_destinatario', 'nombre_destinatario', 'fono').execute()
    
    recipient_list = response.data
    
    if not recipient_list:
        return jsonify({"error": "No recipients found"}), 404
    
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )

    for recipient in recipient_list:
        try:
            message = client.messages.create(
                body=f"Hola, {recipient['nombre_destinatario']}! es un mensaje de prueba",
                from_='+16502002145',
                to=recipient['fono']
            )
            print(f"Message sent to {recipient['nombre_destinatario']} ({recipient['fono']}) - SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send SMS to {recipient['nombre_destinatario']} ({recipient['fono']}): {str(e)}")
    
    return jsonify({"message": "Messages sent successfully to all recipients"},{"destinatarios":response.data}), 200

#################################################### DESTINATARIO 
@user_bp.route('/send_email', methods=['POST'])
def send_emails():
    data = request.json
    id_campana = data.get('id_campana')

    if not id_campana:
        return jsonify({"error": "Falta el ID de la campaña"}), 400

    destinatarios = fetch_destinatarios()
    
    if not destinatarios:
        return jsonify({"error": "No se encontraron destinatarios para esta campaña"}), 404

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
                        sender=create_app.config['MAIL_USERNAME'])

    try:
        mail.send(msg)
        enviados.append({"nombre": nombre, "email": email})
    except Exception as e:
        errores.append({"nombre": nombre, "email": email, "error": str(e)})

    return jsonify({"enviados": enviados, "errores": errores}), 200

########################### AUTH
@user_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña requeridos"}), 400
    
    # Fetch user from Supabase
    user_data = supabase.table('User').select('*').eq('email', email).execute()

    if not user_data.data:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    user = user_data.data[0]

    # Check password
    if not check_password_hash(user['password'], password):
        return jsonify({"error": "contraseña inválida"}), 401
    ##else: 
     ##   if not check_password_hash(user['email'], email):
       ##     return jsonify({"error": "email inválido"}), 401

    return jsonify({"id": user['id']}), 200