from flask import Blueprint, jsonify, request
from .models2 import Campana
import supabase,os
from supabase import Client,create_client

campaign_bp = Blueprint('campaign', __name__)

url = 'https://zwcokbhciyalafyflvkc.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3Y29rYmhjaXlhbGFmeWZsdmtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4OTMzODYsImV4cCI6MjA0NTQ2OTM4Nn0.QWNxXN5_rCDmPNaNpDDHpi5ws4su5XbM8s4ChlhrDGA'
supabase: Client = create_client(url, key)

    
#######################CAMPAÑA POR ID############################################################
@campaign_bp.route('/list_campaigns_by_id', methods=['GET'])
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
    
###########################CREAR CAMPAÑA
@campaign_bp.route('/add_campaigns', methods=['POST'])
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
