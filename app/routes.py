from flask import Blueprint, jsonify, request
from .models2 import User,Campaña
from flask_mail import Mail, Message
import supabase,os
from supabase import Client,create_client
from werkzeug.security import generate_password_hash, check_password_hash
from . import create_app

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
    

@user_bp.route('/list_campaigns_by_id', methods=['GET'])
def fetch_campaigns_by_id():
    user_id = request.args.get('user_id')
    canal = request.args.get('canal')

    if not user_id:
        return jsonify({"error": "Se necesita ID de usuario"}), 400
    if not canal:
        return jsonify({"error": "Se necesita canal"}), 400

    response = supabase.table("Campaña").select("*").eq("user_id", user_id).eq("canal", canal).execute()

    if response.data:
        return jsonify(response.data), 200
    else:
        return jsonify({"error": "No se pudo traer las campañas para este usuario"}), 500


@user_bp.route('/add_campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    campaña = Campaña(**data)  # Create a User instance
    response = supabase.table("Campaña").insert(data).execute()
    if response.data:
        return jsonify(response.data), 200
        print("Response:", response)
    else:
        return jsonify("No se pudo registrar"), 500
        print("Response:", response)




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

    return jsonify({"user_id": user['id']}), 200

