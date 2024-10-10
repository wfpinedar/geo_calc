# persistencia/historial.py

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from configuracion.configuracion import Configuracion

Base = declarative_base()

class Historial(Base):
    __tablename__ = 'historial'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lat1_grados = Column(Float)
    lat1_minutos = Column(Float)
    lat1_segundos = Column(Float)
    lat1_direccion = Column(String)
    lon1_grados = Column(Float)
    lon1_minutos = Column(Float)
    lon1_segundos = Column(Float)
    lon1_direccion = Column(String)
    lat2_grados = Column(Float)
    lat2_minutos = Column(Float)
    lat2_segundos = Column(Float)
    lat2_direccion = Column(String)
    lon2_grados = Column(Float)
    lon2_minutos = Column(Float)
    lon2_segundos = Column(Float)
    lon2_direccion = Column(String)
    distancia = Column(Float)
    rumbo = Column(String)
    azimut = Column(Float)
    fecha = Column(DateTime, default=func.now())
