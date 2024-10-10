# configuracion/configuracion.py

class Configuracion:
    def __init__(self):
        # Valores por defecto
        self.tipo_base_datos = 'sqlite'  # 'sqlite' o 'postgresql'
        self.parametros_conexion = {
            'sqlite': {
                'ruta': 'historial.db'
            },
            'postgresql': {
                'usuario': 'tu_usuario',
                'password': 'tu_contraseña',
                'host': 'localhost',
                'puerto': '5432',
                'base_datos': 'nombre_base_datos'
            }
        }

    def obtener_uri_conexion(self):
        if self.tipo_base_datos == 'sqlite':
            ruta = self.parametros_conexion['sqlite']['ruta']
            return f'sqlite:///{ruta}'
        elif self.tipo_base_datos == 'postgresql':
            params = self.parametros_conexion['postgresql']
            return f"postgresql+psycopg2://{params['usuario']}:{params['password']}@{params['host']}:{params['puerto']}/{params['base_datos']}"
        else:
            raise ValueError('Tipo de base de datos no soportado')
