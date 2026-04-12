from database import get_connection
from entities.context import DimContextEntity

def get_context_by_date(fecha):
    query = """
        SELECT date, is_holiday, es_vispera, day_of_week, temp_max, precipitation
        FROM dim_context
        WHERE date = %s
    """

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (fecha,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return DimContextEntity(
        date=row[0],
        is_holiday=row[1],
        es_vispera=row[2],
        day_of_week=row[3],
        temp_max=float(row[4]) if row[4] else None,
        precipitation=float(row[5]) if row[5] else None
    )