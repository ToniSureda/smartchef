from database import get_connection
from entities.context import DimContextEntity

def get_context_by_date(fecha):
    """ Extraccion de variables de contexto climatico y de calendario filtradas por fecha """
    query = """
        SELECT date, is_holiday, es_vispera, day_of_week, temp_max, precipitation
        FROM dim_context
        WHERE date = %s
    """

    # Apertura de conexion y ejecucion de consulta de lectura especifica
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (fecha,))
    row = cur.fetchone()
    
    # Cierre de sesion y liberacion de recursos del sistema
    conn.close()

    if not row:
        return None

    # Mapeo del registro relacional unico a entidad de dominio estructurada
    return DimContextEntity(
        date=row[0],
        is_holiday=row[1],
        es_vispera=row[2],
        day_of_week=row[3],
        temp_max=float(row[4]) if row[4] else None,
        precipitation=float(row[5]) if row[5] else None
    )