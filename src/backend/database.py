import psycopg2
import os

def get_connection():
    # Usamos la variable de entorno que le pasamos en el docker-compose
    db_url = os.getenv("DATABASE_URL", "postgresql://smartchef:password@db:5432/smartchef")
    return psycopg2.connect(db_url)