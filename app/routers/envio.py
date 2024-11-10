from flask import Blueprint, jsonify, request
import supabase,os
from supabase import Client,create_client
from . import supabase, mail
from flask_mail import Message
from twilio.rest import Client

envio_bp = Blueprint('envio', __name__)

url = 'https://zwcokbhciyalafyflvkc.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3Y29rYmhjaXlhbGFmeWZsdmtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4OTMzODYsImV4cCI6MjA0NTQ2OTM4Nn0.QWNxXN5_rCDmPNaNpDDHpi5ws4su5XbM8s4ChlhrDGA'
supabase: Client = create_client(url, key)



##################################DESTINATARIOS###########
########################################################### SE COMUNICA CON SENDMAIL #######

@envio_bp.route('/destinatarios_list', methods=['GET'])
def fetch_all_destinatarios_from_db():
    """Fetch all recipients from Supabase database."""
    response = supabase.table("Destinatario").select("email", "nombre_destinatario").execute()
    if response.data:
        return response.data
    else:
        return []
    


@envio_bp.route("/send-email", methods=["POST"])
def send_campaign_emails():
    
    id_campana = request.args.get('id_campana')
    email_data = fetch_all_destinatarios_from_db()
    response = supabase.table('Campana').select('template').eq('id_campana', id_campana).execute()

    if response.data:
    # Extract the template string from the response
        template = response.data[0]['template']

    if not email_data:
        return jsonify({"error": "Se necesitan destinatarios"}), 400

    if not id_campana:
        return jsonify({"error": "Se necesita ID de la campaña"}), 400

    try:
        sent_emails = []
        for email_info in email_data:
            email_destinatario = email_info['email']
            nombre_destinatario = email_info['nombre_destinatario']
            
            subject = f"HOLA ESTIMADO {nombre_destinatario} !!"
            body = template

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
@envio_bp.route('/send-sms', methods=['POST'])  # Change GET to POST
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

