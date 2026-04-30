import psycopg2
import os

def get_connection():
    # Extraccion de la cadena de conexion estrictamente desde variables de entorno
    db_url = os.getenv("DATABASE_URL")
    
    #si no hay .env no se conecta
    if not db_url:
        raise ValueError("Variable DATABASE_URL no está configurada en el entorno.")
        
    return psycopg2.connect(db_url)