import psycopg2
import os

def get_connection():
    # Extraccion de la cadena de conexion desde variables de entorno con fallback a configuracion local
    db_url = os.getenv("DATABASE_URL", "postgresql://smartchef:password@db:5432/smartchef")
    return psycopg2.connect(db_url)