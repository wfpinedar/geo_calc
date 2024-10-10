import sqlite3
import psycopg2

class BaseDatos:
    def __init__(self, tipo):
        self.tipo = tipo
        self.conexion = self.conectar()

    def conectar(self):
        if self.tipo == "sqlite":
            return sqlite3.connect("historial.db")
        elif self.tipo == "postgresql":
            # Configurar conexión a PostgreSQL
            return psycopg2.connect(
                dbname="database",
                user="postgres",
                password="12345",
                host="localhost"
            )
        else:
            raise ValueError("Tipo de base de datos no soportado")
