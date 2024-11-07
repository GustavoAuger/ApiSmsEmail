from flask import Blueprint, jsonify, request,app
from .models2 import User,Campana,Envio,Envio_destinatario,Destinatario
from flask_mail import Message
import supabase,os
from supabase import Client,create_client
from werkzeug.security import generate_password_hash, check_password_hash
from . import create_app,mail
from twilio.rest import Client

report_bp = Blueprint('report', __name__)

url = 'https://zwcokbhciyalafyflvkc.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3Y29rYmhjaXlhbGFmeWZsdmtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4OTMzODYsImV4cCI6MjA0NTQ2OTM4Nn0.QWNxXN5_rCDmPNaNpDDHpi5ws4su5XbM8s4ChlhrDGA'
supabase: Client = create_client(url, key)
##APIs POR INTEGAR Y DIVIDIR POR SERVICIO CORRESPONDIENTE --- EN DESARROOLLO / FALTA IMPLEMENTAR EN FRONT


@report_bp.route('/add_user', methods=['POST'])
def create_user():
    data = request.json
    password = request.json.get('password')
    hashed_password = generate_password_hash(password)  
    data['password'] = hashed_password 
    user = User(**data)  # Create a User instance
    response = supabase.table("User").insert(data).execute()
    if response.data:
        return jsonify(response.data), 200
 
    else:
        return jsonify("No se pudo traer a los usuarios"), 500
       

@report_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    user_id = data.get("id")  # Extract user ID from the JSON payload
    if not user_id:
        return {"error": "User ID is required"}
      
    response = supabase.table("User").delete().eq("id", user_id).execute()
    if response.data:
        return jsonify(response.data), 200
    else:
        return jsonify("No se pudo borrar el usuario"), 500
        

@report_bp.route('/update_user/<user_id>', methods=['PUT'])
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
    


    
#############################################################
# ###################### GET ENVIOS ######################   
@report_bp.route("/send_instances", methods=["GET"])
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
@report_bp.route("/intermediary_records", methods=["GET"])
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

