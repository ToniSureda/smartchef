import pandas as pd
from database import get_connection

def get_historico_compras():
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

    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df