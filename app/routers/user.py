from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models2 import User
import supabase,os
from supabase import Client,create_client
user_bp = Blueprint('user', __name__)

url = 'https://zwcokbhciyalafyflvkc.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3Y29rYmhjaXlhbGFmeWZsdmtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4OTMzODYsImV4cCI6MjA0NTQ2OTM4Nn0.QWNxXN5_rCDmPNaNpDDHpi5ws4su5XbM8s4ChlhrDGA'
supabase: Client = create_client(url, key)

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

