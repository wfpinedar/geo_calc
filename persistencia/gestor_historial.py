# persistencia/gestor_historial.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from persistencia.historial import Base, Historial
from configuracion.configuracion import Configuracion

class GestorHistorial:
    def __init__(self):
        self.config = Configuracion()
        self.uri_conexion = self.config.obtener_uri_conexion()
        self.engine = create_engine(self.uri_conexion)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def guardar_registro(self, punto1, punto2, distancia, rumbo, azimut):
        session = self.Session()
        registro = Historial(
            lat1_grados=punto1.latitud.grados,
            lat1_minutos=punto1.latitud.minutos,
            lat1_segundos=punto1.latitud.segundos,
            lat1_direccion=punto1.latitud.direccion,
            lon1_grados=punto1.longitud.grados,
            lon1_minutos=punto1.longitud.minutos,
            lon1_segundos=punto1.longitud.segundos,
            lon1_direccion=punto1.longitud.direccion,
            lat2_grados=punto2.latitud.grados,
            lat2_minutos=punto2.latitud.minutos,
            lat2_segundos=punto2.latitud.segundos,
            lat2_direccion=punto2.latitud.direccion,
            lon2_grados=punto2.longitud.grados,
            lon2_minutos=punto2.longitud.minutos,
            lon2_segundos=punto2.longitud.segundos,
            lon2_direccion=punto2.longitud.direccion,
            distancia=distancia,
            rumbo=rumbo,
            azimut=azimut
        )
        session.add(registro)
        session.commit()
        session.close()

    def obtener_registros(self):
        session = self.Session()
        registros = session.query(Historial).order_by(Historial.fecha.desc()).all()
        session.close()
        return registros
    
    def obtener_un_registro(self, id):
        session = self.Session()
        registro = session.query(Historial).filter(Historial.id == id).one()
        session.close()
        return registro
    
    def eliminar_registro(self, id):
        session = self.Session()
        try:
            session.query(Historial).filter(Historial.id == id).delete(synchronize_session="evaluate")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar: {e}")
        finally:
            session.close()
    
    def actualizar_registro(self, id, updated_registro):
        session = self.Session()
        try:
            session.query(Historial).filter(Historial.id == id).update(
                updated_registro,
                synchronize_session="fetch"
            )
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error al actualizar: {e}")
        finally:
            session.close()

    def cerrar_conexion(self):
        self.engine.dispose()
