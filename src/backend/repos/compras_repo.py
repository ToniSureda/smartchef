import pandas as pd
from database import get_connection

def get_historico_compras():
    """ Extraccion del registro historico de transacciones estructurado en un DataFrame """
    query = """
    SELECT
        fecha,
        id_ticket,
        turno,
        id_plato,
        cantidad
    FROM fact_sales
    ORDER BY fecha, id_ticket;
    """

    # Establecimiento de conexion y carga directa del conjunto de resultados en memoria
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    
    # Cierre de la sesion con la base de datos para liberar recursos
    conn.close()

    return df