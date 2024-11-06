from sqlalchemy import Boolean, Integer,String,ForeignKey,Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True)
    cliente_name = Column(String, nullable=False)
    cliente_apellido = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    fono = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False,unique=False)

class Campana(Base):
    __tablename__ = 'Campana'
    
    id = Column(Integer, primary_key=True)
    nombre_campaña = Column(String, nullable=False)
    templete = Column(String, nullable=False)
    canal = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    reporte_id = Column(Integer, ForeignKey('Reporte.id'), nullable=True)

class Reporte(Base):
    __tablename__ = 'Reporte'
    
    id = Column(Integer, primary_key=True)
    fallidos = Column(Integer, default=0)
    errores = Column(Integer, default=0)
    enviados = Column(Integer, default=0)
    rebotes = Column(Integer, default=0)
    campana_id = Column(Integer, ForeignKey('Campana.id'), nullable=True)

class Envio(Base):
    __tablename__ = 'Envio'
    
    id = Column(Integer, primary_key=True)
    tipo_envio = Column(Boolean,nullable=False)
    fk_id_campana = Column(Integer, ForeignKey('Campana.id'), nullable=True)

class Envio_destinatario(Base):
    __tablename__ = 'Envio_destinatario'
    
    id = Column(Integer, primary_key=True)
    fk_envio = Column(Integer, ForeignKey('Envio.id'), nullable=True)
    fk_destinatario = Column(Integer, ForeignKey('Destinatario.id'), nullable=True)

class Destinatario(Base):
    __tablename__ = 'Destinatario'
    
    id = Column(Integer, primary_key=True)
    nombre_destinatario = Column(String, primary_key=True)
    tipo_envio = Column(Boolean,nullable=False)
    fk_id_campana = Column(Integer, ForeignKey('Campana.id'), nullable=True)


