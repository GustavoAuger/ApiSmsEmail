from sqlalchemy import Boolean, Integer,String,ForeignKey,Column
from sqlalchemy.orm import relationship,declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True)
    cliente_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    fono = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False,unique=False)

"""def get_users():
    response = supabase.table("User").select("*").execute()
    return response.data

def add_user(user: User):
    response = supabase.table("User").insert(user.__dict__).execute()
    return response.data"""

"""def update_user(user_id: str, user: User):
    response = supabase.from_("User").update(user.__dict__).eq("id", user_id).execute()
    return response.data

def delete_user(user_id: str):
    response = supabase.from_("User").delete().eq("id", user_id).execute()
    return response.data"""

class Campaña(Base):
    __tablename__ = 'Campaña'
    
    id = Column(Integer, primary_key=True)
    nombre_campaña = Column(String, nullable=False)
    estado = Column(Boolean, nullable=False)
    canal = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    reporte_id = Column(Integer, ForeignKey('Reporte.id'), nullable=True)

class Reporte(Base):
    __tablename__ = 'Reporte'
    
    id = Column(Integer, primary_key=True)
    fallidos = Column(Integer, default=0)
    errores = Column(Integer, default=0)
    enviados = Column(Integer, default=0)
    rebotes = Column(Integer, default=0)
    campaña_id = Column(Integer, ForeignKey('Campaña.id'), nullable=True)


