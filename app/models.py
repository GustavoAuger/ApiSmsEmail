import supabase
import uuid

class User:
    def __init__(self, email: str, name: str, password: str,id: int=None):
        self.id = int(uuid.uuid4()) if id is None else id
        self.email = email
        self.name = name
        self.password = password

def get_users():
    response = supabase.table("user").select("*").execute()
    return response.data

def add_user(user: User):
    response = supabase.table("user").insert(user.__dict__).execute()
    return response.data

def update_user(user_id: str, user: User):
    response = supabase.table("user").update(user.__dict__).eq("id", user_id).execute()
    return response.data

def delete_user(user_id: str):
    response = supabase.table("user").delete().eq("id", user_id).execute()
    return response.data

class Campaign:
    def __init__(self, user_id: int, nombre: str, canal: bool, estado: bool, id: int = None,report_id: int = None):
        self.id = int(uuid.uuid4()) if id is None else id  
        self.user_id = user_id
        self.nombre = nombre
        self.canal = canal
        self.estado = estado
        self.report_id = report_id

def get_campaigns():
    response = supabase.table("campaigns").select("*").execute()
    return response.data

def add_campaign(campaign: Campaign):
    response = supabase.table("campaigns").insert(campaign.__dict__).execute()
    return response.data

def update_campaign(campaign_id: str, campaign: Campaign):
    response = supabase.table("campaigns").update(campaign.__dict__).eq("id", campaign_id).execute()
    return response.data

def delete_campaign(campaign_id: str):
    response = supabase.table("campaigns").delete().eq("id", campaign_id).execute()
    return response.data


class Reporte:
    def __init__(self, enviados: int, fallidos: int, errores: int, rebotes: int, id: int = None,campaign_id: int = None):
        self.id = int(uuid.uuid4()) if id is None else id
        self.enviados = enviados
        self.fallidos = fallidos
        self.errores = errores
        self.rebotes = rebotes
        self.campaign_id = campaign_id

def get_reportes():
    response = supabase.table("reports").select("*").execute()
    return response.data

def add_reporte(report: Reporte):
    response = supabase.table("reports").insert(report.__dict__).execute()
    return response.data

def update_reporte(report_id: str, report: Reporte):
    response = supabase.table("reports").update(report.__dict__).eq("id", report_id).execute()
    return response.data

def delete_reporte(report_id: str):
    response = supabase.table("reports").delete().eq("id", report_id).execute()
    return response.data